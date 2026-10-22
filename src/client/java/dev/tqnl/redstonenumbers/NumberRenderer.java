package dev.tqnl.redstonenumbers;

import com.mojang.blaze3d.vertex.PoseStack;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.rendering.v1.FabricRenderState;
import net.fabricmc.fabric.api.client.rendering.v1.RenderStateDataKey;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelExtractionContext;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelRenderContext;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.navigation.ScreenRectangle;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FontDescription;
import net.minecraft.network.chat.Style;
import net.minecraft.resources.Identifier;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.phys.Vec3;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/** Adds only ordinary depth-tested world text to Minecraft's existing submit queue. */
public final class NumberRenderer {
    private static final RenderStateDataKey<Frame> FRAME = RenderStateDataKey.create(() -> "redstonenumbers:labels");
    private static final Style NUMBER_STYLE = Style.EMPTY.withFont(new FontDescription.Resource(
            Identifier.fromNamespaceAndPath("redstonenumbers", "numbers"))).withoutShadow();
    private static final float GLYPH_HEIGHT = 16.0F;
    private static final float BLOCK_SIZE = 0.25F;
    private static final float VISIBLE_GLYPH_HEIGHT = 12.0F;
    // The dust surface is at Y=0.25/16; the label anchor starts just above it.
    // Use that anchor with a small physical clearance, rather than the wire's collision height.
    private static final double SURFACE_CLEARANCE = 0.251 / 16.0 + 1.0 / 512.0;
    private List<Glyph> glyphs;

    public void invalidateFont() {
        glyphs = null;
    }

    public void extract(LevelExtractionContext context, ModConfig config) {
        FabricRenderState state = (FabricRenderState) context.levelState();
        Minecraft client = Minecraft.getInstance();
        if (!config.enabled || context.level() == null) {
            state.setData(FRAME, null);
            return;
        }

        CameraRenderState camera = context.levelState().cameraRenderState;
        List<WireIndex.Label> labels = WireIndex.INSTANCE.snapshot(
                context.level(), camera.pos, camera.cullFrustum, config.range, config.maxLabels);
        if (labels.isEmpty()) {
            state.setData(FRAME, null);
            return;
        }
        if (glyphs == null) {
            glyphs = measureGlyphs(client.font);
        }
        Quaternionf orientation = camera.orientation;
        Vector3f up = new Vector3f(0, 1, 0).rotate(orientation);
        Vector3f right = new Vector3f(1, 0, 0).rotate(orientation);
        float units = BLOCK_SIZE * config.scale / GLYPH_HEIGHT;
        // The artwork's first/last two rows are transparent. Lift only the visible ink
        // above the dust; counting those margins made the labels appear to hover.
        // The width term also handles camera roll supplied by another mod.
        double lift = SURFACE_CLEARANCE + units * 0.5
                * (VISIBLE_GLYPH_HEIGHT * Math.abs(up.y) + GLYPH_HEIGHT * Math.abs(right.y));
        state.setData(FRAME, new Frame(List.copyOf(labels), glyphs, camera.pos,
                orientation.x, orientation.y, orientation.z, orientation.w, units, lift));
    }

    public void submit(LevelRenderContext context) {
        Frame frame = ((FabricRenderState) context.levelState()).getData(FRAME);
        if (frame == null) {
            return;
        }
        PoseStack poses = context.poseStack();
        Quaternionf orientation = new Quaternionf(frame.qx, frame.qy, frame.qz, frame.qw);
        for (WireIndex.Label label : frame.labels) {
            Glyph glyph = frame.glyphs.get(label.power());
            poses.pushPose();
            // Subtract in double precision before PoseStack converts to floats, including at distant coordinates.
            poses.translate(label.position().getX() + 0.5 - frame.camera.x,
                    label.position().getY() + frame.lift - frame.camera.y,
                    label.position().getZ() + 0.5 - frame.camera.z);
            poses.rotate(orientation);
            poses.scale(frame.units, -frame.units, frame.units);
            context.submitNodeCollector().submitText(poses, glyph.x, glyph.y, glyph.text, false,
                    Font.DisplayMode.NORMAL, label.packedLight(), 0xFFFFFFFF, 0, 0);
            poses.popPose();
        }
    }

    private static List<Glyph> measureGlyphs(Font font) {
        List<Glyph> result = new ArrayList<>(16);
        for (int power = 0; power < 16; power++) {
            FormattedCharSequence text = Component.literal(String.valueOf((char) (0xE000 + power)))
                    .setStyle(NUMBER_STYLE).getVisualOrderText();
            ScreenRectangle bounds = font.prepareText(text, 0, 0, 0xFFFFFFFF, false, false, 0).bounds();
            // Measure the bitmap rectangle, rather than advance (which includes a trailing spacing pixel).
            float x = bounds == null ? -font.width(text) / 2.0F : -bounds.left() - bounds.width() / 2.0F;
            float y = bounds == null ? 1.0F : -bounds.top() - bounds.height() / 2.0F;
            result.add(new Glyph(text, x, y));
        }
        return List.copyOf(result);
    }

    private record Glyph(FormattedCharSequence text, float x, float y) { }

    private record Frame(List<WireIndex.Label> labels, List<Glyph> glyphs, Vec3 camera,
                         float qx, float qy, float qz, float qw, float units, double lift) { }
}
