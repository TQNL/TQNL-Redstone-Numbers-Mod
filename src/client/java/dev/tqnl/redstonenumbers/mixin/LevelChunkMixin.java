package dev.tqnl.redstonenumbers.mixin;

import dev.tqnl.redstonenumbers.WireIndex;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(LevelChunk.class)
abstract class LevelChunkMixin {
    @Inject(method = "setBlockState", at = @At("RETURN"))
    private void redstonenumbers$observeSuccessfulChange(BlockPos position, BlockState state, int flags,
            CallbackInfoReturnable<BlockState> callback) {
        if (callback.getReturnValue() != null
                && ((LevelChunk) (Object) this).getLevel() instanceof ClientLevel level) {
            WireIndex.INSTANCE.onBlockChanged(level, position, state);
        }
    }
}
