package dev.tqnl.redstonenumbers;

import java.util.Locale;
import net.caffeinemc.mods.sodium.api.config.ConfigEntryPoint;
import net.caffeinemc.mods.sodium.api.config.StorageEventHandler;
import net.caffeinemc.mods.sodium.api.config.option.OptionFlag;
import net.caffeinemc.mods.sodium.api.config.structure.ConfigBuilder;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;

/** Optional native options; Sodium and compatible layouts own the controls and pending edits. */
public final class SodiumIntegration implements ConfigEntryPoint {
    @Override
    public void registerConfigLate(ConfigBuilder builder) {
        var config = RedstoneNumbersClient.config();
        StorageEventHandler save = RedstoneNumbersClient::saveConfig;
        var options = builder.registerOwnModOptions();
        var icon = id("icon.png");
        try {
            options.setNonTintedIcon(icon);
        } catch (NoSuchMethodError olderApi) {
            options.setIcon(icon);
        }
        options.addPage(builder.createOptionPage()
                .setName(Component.translatable("screen.redstonenumbers.options"))
                .addOption(builder.createBooleanOption(id("enabled"))
                        .setName(text("enabled"))
                        .setTooltip(text("enabled.help"))
                        .setStorageHandler(save)
                        .setBinding(value -> config.enabled = value, () -> config.enabled)
                        .setDefaultValue(true))
                .addOption(builder.createIntegerOption(id("range"))
                        .setName(text("range"))
                        .setTooltip(text("range.help"))
                        .setStorageHandler(save)
                        .setBinding(value -> config.range = value, () -> config.range)
                        .setDefaultValue(16)
                        .setRange(1, 128, 1)
                        .setValueFormatter(value -> Component.literal(Integer.toString(value))))
                .addOption(builder.createIntegerOption(id("limit"))
                        .setName(text("limit"))
                        .setTooltip(text("limit.help"))
                        .setStorageHandler(save)
                        .setBinding(value -> config.maxLabels = value, () -> config.maxLabels)
                        .setDefaultValue(1024)
                        .setRange(1, 65536, 1)
                        .setValueFormatter(value -> Component.literal(Integer.toString(value))))
                .addOption(builder.createIntegerOption(id("scale"))
                        .setName(text("scale"))
                        .setTooltip(text("scale.help"))
                        .setStorageHandler(save)
                        .setBinding(value -> config.scale = value / 100.0F,
                                () -> Math.round(config.scale * 100.0F))
                        .setDefaultValue(100)
                        .setRange(25, 400, 1)
                        .setValueFormatter(value -> Component.literal(
                                String.format(Locale.ROOT, "%.2f", value / 100.0F))))
                .addOption(builder.createBooleanOption(id("show_pack"))
                        .setName(text("show_pack"))
                        .setTooltip(text("show_pack.help"))
                        .setStorageHandler(save)
                        .setBinding(value -> config.showBuiltinPack = value, () -> config.showBuiltinPack)
                        .setDefaultValue(true)
                        .setFlags(OptionFlag.REQUIRES_GAME_RESTART)));
    }

    private static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath("redstonenumbers", path);
    }

    private static Component text(String option) {
        return Component.translatable("screen.redstonenumbers." + option);
    }
}
