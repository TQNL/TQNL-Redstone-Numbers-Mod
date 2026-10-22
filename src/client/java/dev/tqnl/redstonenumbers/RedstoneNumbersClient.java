package dev.tqnl.redstonenumbers;

import com.mojang.blaze3d.platform.InputConstants;
import java.nio.file.Path;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientChunkEvents;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelRenderEvents;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.fabricmc.fabric.api.resource.v1.pack.PackActivationType;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class RedstoneNumbersClient implements ClientModInitializer {
    public static final Logger LOGGER = LoggerFactory.getLogger("redstonenumbers");
    private static ModConfig config;
    private static Path configPath;
    private final NumberRenderer renderer = new NumberRenderer();
    private ClientLevel previousLevel;

    @Override
    public void onInitializeClient() {
        configPath = FabricLoader.getInstance().getConfigDir().resolve("redstonenumbers.json");
        config = ModConfig.load(configPath);
        VideoSettingsIntegration.register();
        ResourceLoader.registerBuiltinPack(
                Identifier.fromNamespaceAndPath("redstonenumbers", "clean_lines"),
                FabricLoader.getInstance().getModContainer("redstonenumbers").orElseThrow(),
                Component.translatable("pack.redstonenumbers.clean_lines.title"), PackActivationType.NORMAL);
        KeyMapping.Category category = KeyMapping.Category.register(
                Identifier.fromNamespaceAndPath("redstonenumbers", "controls"));
        KeyMapping toggle = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.redstonenumbers.toggle",
                InputConstants.Type.KEYSYM, InputConstants.UNKNOWN.getValue(), category));
        KeyMapping settings = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.redstonenumbers.settings",
                InputConstants.Type.KEYSYM, InputConstants.UNKNOWN.getValue(), category));

        ClientChunkEvents.CHUNK_LOAD.register(WireIndex.INSTANCE::onChunkLoad);
        ClientChunkEvents.CHUNK_UNLOAD.register(WireIndex.INSTANCE::onChunkUnload);
        ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> {
            WireIndex.INSTANCE.reset();
            previousLevel = null;
        });
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (toggle.consumeClick()) {
                config.enabled = !config.enabled;
                config.save(configPath);
                if (client.player != null) {
                    client.player.sendOverlayMessage(Component.translatable(config.enabled
                            ? "message.redstonenumbers.enabled" : "message.redstonenumbers.disabled"));
                }
            }
            while (settings.consumeClick()) {
                client.setScreen(createSettingsScreen(client.screen));
            }
            if (client.level != previousLevel) {
                WireIndex.INSTANCE.reset();
                previousLevel = client.level;
            }
            if (client.level != null) {
                Vec3 camera = client.gameRenderer.getMainCamera().isInitialized()
                        ? client.gameRenderer.getMainCamera().position()
                        : client.player == null ? Vec3.ZERO : client.player.position();
                WireIndex.INSTANCE.tick(client.level, camera, config.range, config.enabled);
            }
        });
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(
                Identifier.fromNamespaceAndPath("redstonenumbers", "font_layout"),
                (ResourceManagerReloadListener) resources -> renderer.invalidateFont());
        LevelRenderEvents.END_EXTRACTION.register(context -> renderer.extract(context, config));
        LevelRenderEvents.COLLECT_SUBMITS.register(renderer::submit);
        LOGGER.info("Redstone Numbers ready: ordinary world text, range {}, limit {}", config.range, config.maxLabels);
    }

    static ModConfig config() {
        return config;
    }

    static void saveConfig() {
        config.save(configPath);
    }

    public static Screen createSettingsScreen(Screen parent) {
        return new SettingsScreen(parent, config, configPath);
    }
}
