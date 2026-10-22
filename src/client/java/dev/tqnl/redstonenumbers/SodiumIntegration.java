package dev.tqnl.redstonenumbers;

import net.caffeinemc.mods.sodium.api.config.ConfigEntryPoint;
import net.caffeinemc.mods.sodium.api.config.structure.ConfigBuilder;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;

/** Optional Sodium API entrypoint; the native settings screen remains the single editor. */
public final class SodiumIntegration implements ConfigEntryPoint {
    @Override
    public void registerConfigLate(ConfigBuilder builder) {
        var options = builder.registerOwnModOptions();
        var icon = Identifier.fromNamespaceAndPath("redstonenumbers", "icon.png");
        try {
            options.setNonTintedIcon(icon);
        } catch (NoSuchMethodError olderApi) {
            // Earlier config APIs, including Sodium 0.8.0, expose only tinted icons.
            options.setIcon(icon);
        }
        options.addPage(builder.createExternalPage()
                        .setName(Component.translatable("options.title"))
                        .setScreenConsumer(parent -> Minecraft.getInstance().setScreen(
                                RedstoneNumbersClient.createSettingsScreen(parent))));
    }
}
