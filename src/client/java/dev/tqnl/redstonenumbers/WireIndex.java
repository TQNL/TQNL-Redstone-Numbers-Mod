package dev.tqnl.redstonenumbers;

import it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap;
import it.unimi.dsi.fastutil.longs.LongIterator;
import it.unimi.dsi.fastutil.longs.LongOpenHashSet;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.core.BlockPos;
import net.minecraft.core.SectionPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.RedStoneWireBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import net.minecraft.world.level.chunk.LevelChunkSection;
import net.minecraft.world.level.chunk.status.ChunkStatus;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Client-thread-only index of wire positions in the sections around the camera. */
public final class WireIndex {
    public static final WireIndex INSTANCE = new WireIndex();

    private static final int BLOCKS_PER_SECTION = 4096;
    private static final int SECTIONS_PER_TICK = 8;
    private static final long SCAN_BUDGET_NANOS = 1_000_000L;
    private static final Comparator<Candidate> NEAREST_FIRST = Comparator
            .comparingDouble(Candidate::distanceSquared)
            .thenComparingLong(Candidate::position);

    private final Long2ObjectOpenHashMap<IndexedSection> sections = new Long2ObjectOpenHashMap<>();
    private final PriorityQueue<IndexedSection> pending = new PriorityQueue<>(Comparator
            .comparingDouble((IndexedSection section) -> section.distanceSquared)
            .thenComparingLong(section -> section.key));
    private ClientLevel currentLevel;
    private Bounds currentBounds;
    private BlockPos lastPriorityPosition;
    private boolean enabled;
    private boolean regionDirty;

    private WireIndex() {}

    public void tick(ClientLevel level, Vec3 cameraPosition, int range, boolean enabled) {
        if (!enabled || level == null) {
            if (this.enabled || currentLevel != null) {
                reset();
            }
            return;
        }
        if (level != currentLevel) {
            reset();
            currentLevel = level;
            this.enabled = true;
            regionDirty = true;
        }

        Bounds bounds = Bounds.around(level, cameraPosition, range);
        BlockPos priorityPosition = BlockPos.containing(cameraPosition);
        if (regionDirty || !bounds.equals(currentBounds)) {
            rebuildRegion(level, cameraPosition, bounds);
        } else if (!pending.isEmpty() && !priorityPosition.equals(lastPriorityPosition)) {
            reprioritize(cameraPosition);
        }
        lastPriorityPosition = priorityPosition;
        scanPending();
    }

    /** The returned records contain no live world or chunk references. */
    public List<Label> snapshot(ClientLevel level, Vec3 cameraPosition, Frustum frustum,
            int range, int maxLabels) {
        if (!enabled || level != currentLevel || maxLabels <= 0) {
            return List.of();
        }

        double rangeSquared = (double) range * range;
        PriorityQueue<Candidate> nearest = new PriorityQueue<>(NEAREST_FIRST.reversed());
        for (IndexedSection section : sections.values()) {
            LongIterator positions = section.wires.iterator();
            while (positions.hasNext()) {
                long packed = positions.nextLong();
                int x = BlockPos.getX(packed);
                int y = BlockPos.getY(packed);
                int z = BlockPos.getZ(packed);
                double distanceSquared = cameraPosition.distanceToSqr(x + 0.5, y + 0.05, z + 0.5);
                if (distanceSquared > rangeSquared) {
                    continue;
                }
                // Covers the complete billboard at the maximum supported scale and camera pitch.
                if (frustum != null && !frustum.isVisible(new AABB(
                        x - 0.25, y - 0.05, z - 0.25, x + 1.25, y + 1.55, z + 1.25))) {
                    continue;
                }

                BlockPos position = BlockPos.of(packed);
                BlockState state = section.chunk.getBlockState(position);
                if (!state.is(Blocks.REDSTONE_WIRE)) {
                    positions.remove();
                    continue;
                }
                Candidate candidate = new Candidate(packed, distanceSquared,
                        state.getValue(RedStoneWireBlock.POWER));
                if (nearest.size() < maxLabels) {
                    nearest.add(candidate);
                } else if (NEAREST_FIRST.compare(candidate, nearest.peek()) < 0) {
                    nearest.poll();
                    nearest.add(candidate);
                }
            }
        }

        List<Candidate> ordered = new ArrayList<>(nearest);
        ordered.sort(NEAREST_FIRST);
        List<Label> labels = new ArrayList<>(ordered.size());
        for (Candidate candidate : ordered) {
            BlockPos position = BlockPos.of(candidate.position);
            labels.add(new Label(position, candidate.power, LevelRenderer.getLightColor(level, position)));
        }
        return List.copyOf(labels);
    }

    public void onChunkLoad(ClientLevel level, LevelChunk chunk) {
        if (!enabled || level != currentLevel) {
            return;
        }
        // A full packet may replace data in the same LevelChunk object. Always rescan that column.
        removeChunk(chunk, false);
        regionDirty = true;
    }

    public void onChunkUnload(ClientLevel level, LevelChunk chunk) {
        if (!enabled || level != currentLevel) {
            return;
        }
        removeChunk(chunk, true);
        regionDirty = true;
    }

    /** Observe successful block changes without modifying any world state or update behaviour. */
    public void onBlockChanged(ClientLevel level, BlockPos position, BlockState state) {
        if (!enabled || level != currentLevel) {
            return;
        }
        IndexedSection section = sections.get(SectionPos.asLong(position));
        if (section == null) {
            return;
        }
        if (state.is(Blocks.REDSTONE_WIRE)) {
            section.wires.add(position.asLong());
        } else {
            section.wires.remove(position.asLong());
        }
    }

    public void reset() {
        enabled = false;
        currentLevel = null;
        currentBounds = null;
        lastPriorityPosition = null;
        regionDirty = false;
        sections.clear();
        pending.clear();
    }

    private void rebuildRegion(ClientLevel level, Vec3 cameraPosition, Bounds bounds) {
        LongOpenHashSet retained = new LongOpenHashSet();
        pending.clear();
        for (int x = bounds.minX; x <= bounds.maxX; x++) {
            for (int z = bounds.minZ; z <= bounds.maxZ; z++) {
                LevelChunk chunk = level.getChunkSource().getChunk(x, z, ChunkStatus.FULL, false);
                if (chunk == null) {
                    continue;
                }
                for (int y = bounds.minY; y <= bounds.maxY; y++) {
                    long key = SectionPos.asLong(x, y, z);
                    retained.add(key);
                    IndexedSection section = sections.get(key);
                    if (section == null || section.chunk != chunk) {
                        section = new IndexedSection(key, chunk, y);
                        sections.put(key, section);
                    }
                    if (section.nextBlock < BLOCKS_PER_SECTION) {
                        section.updateDistance(cameraPosition);
                        pending.add(section);
                    }
                }
            }
        }
        sections.keySet().retainAll(retained);
        currentBounds = bounds;
        regionDirty = false;
    }

    private void reprioritize(Vec3 cameraPosition) {
        List<IndexedSection> entries = new ArrayList<>(pending);
        pending.clear();
        for (IndexedSection section : entries) {
            section.updateDistance(cameraPosition);
            pending.add(section);
        }
    }

    private void scanPending() {
        long deadline = System.nanoTime() + SCAN_BUDGET_NANOS;
        int completed = 0;
        while (completed < SECTIONS_PER_TICK && !pending.isEmpty()) {
            IndexedSection entry = pending.peek();
            LevelChunkSection section = entry.chunk.getSection(
                    entry.chunk.getSectionIndexFromSectionY(entry.sectionY));
            if (entry.nextBlock == 0 && (section.hasOnlyAir()
                    || !section.maybeHas(state -> state.is(Blocks.REDSTONE_WIRE)))) {
                entry.nextBlock = BLOCKS_PER_SECTION;
            }
            int baseX = entry.chunk.getPos().getMinBlockX();
            int baseY = entry.sectionY << 4;
            int baseZ = entry.chunk.getPos().getMinBlockZ();
            while (entry.nextBlock < BLOCKS_PER_SECTION) {
                int index = entry.nextBlock++;
                int x = index & 15;
                int y = index >> 8;
                int z = (index >> 4) & 15;
                long position = BlockPos.asLong(baseX + x, baseY + y, baseZ + z);
                if (section.getBlockState(x, y, z).is(Blocks.REDSTONE_WIRE)) {
                    entry.wires.add(position);
                } else {
                    entry.wires.remove(position);
                }
                // Partial sections continue next tick; the deadline check itself stays inexpensive.
                if ((entry.nextBlock & 127) == 0 && System.nanoTime() >= deadline) {
                    return;
                }
            }
            pending.poll();
            completed++;
            if (System.nanoTime() >= deadline) {
                return;
            }
        }
    }

    private void removeChunk(LevelChunk chunk, boolean requireSameInstance) {
        int x = chunk.getPos().x;
        int z = chunk.getPos().z;
        sections.values().removeIf(section -> section.chunk.getPos().x == x
                && section.chunk.getPos().z == z && (!requireSameInstance || section.chunk == chunk));
        pending.removeIf(section -> section.chunk.getPos().x == x
                && section.chunk.getPos().z == z && (!requireSameInstance || section.chunk == chunk));
    }

    public record Label(BlockPos position, int power, int packedLight) {}

    private record Candidate(long position, double distanceSquared, int power) {}

    private record Bounds(int minX, int minY, int minZ, int maxX, int maxY, int maxZ) {
        private static Bounds around(ClientLevel level, Vec3 position, int range) {
            return new Bounds(
                    SectionPos.posToSectionCoord(position.x - range),
                    Math.max(level.getMinSectionY(), SectionPos.posToSectionCoord(position.y - range)),
                    SectionPos.posToSectionCoord(position.z - range),
                    SectionPos.posToSectionCoord(position.x + range),
                    Math.min(level.getMaxSectionY(), SectionPos.posToSectionCoord(position.y + range)),
                    SectionPos.posToSectionCoord(position.z + range));
        }
    }

    private static final class IndexedSection {
        private final long key;
        private final LevelChunk chunk;
        private final int sectionY;
        private final LongOpenHashSet wires = new LongOpenHashSet();
        private int nextBlock;
        private double distanceSquared;

        private IndexedSection(long key, LevelChunk chunk, int sectionY) {
            this.key = key;
            this.chunk = chunk;
            this.sectionY = sectionY;
        }

        private void updateDistance(Vec3 cameraPosition) {
            distanceSquared = cameraPosition.distanceToSqr(chunk.getPos().getMinBlockX() + 8.0,
                    (sectionY << 4) + 8.0, chunk.getPos().getMinBlockZ() + 8.0);
        }
    }
}
