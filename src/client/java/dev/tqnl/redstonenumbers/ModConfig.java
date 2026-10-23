package dev.tqnl.redstonenumbers;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Shared client settings, previewed live and persisted only when accepted. */
public final class ModConfig {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    public boolean enabled = true;
    public boolean showBuiltinPack = true;
    public int range = 16;
    public int maxLabels = 1024;
    public float scale = 1.0F;

    public static ModConfig load(Path path) {
        if (!Files.exists(path)) {
            ModConfig defaults = new ModConfig();
            defaults.save(path);
            return defaults;
        }
        try (Reader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            ModConfig config = GSON.fromJson(reader, ModConfig.class);
            if (config == null) {
                throw new IllegalArgumentException("Expected a JSON object");
            }
            config.sanitize();
            return config;
        } catch (IOException | RuntimeException exception) {
            RedstoneNumbersClient.LOGGER.warn("Cannot read redstonenumbers.json; using defaults and preserving the existing file", exception);
            return new ModConfig();
        }
    }

    public void sanitize() {
        range = Math.clamp(range, 1, 128);
        maxLabels = Math.clamp(maxLabels, 1, 65536);
        scale = Float.isFinite(scale) ? Math.clamp(scale, 0.25F, 4.0F) : 1.0F;
    }

    public ModConfig copy() {
        ModConfig copy = new ModConfig();
        copy.copyFrom(this);
        return copy;
    }

    public void copyFrom(ModConfig other) {
        enabled = other.enabled;
        showBuiltinPack = other.showBuiltinPack;
        range = other.range;
        maxLabels = other.maxLabels;
        scale = other.scale;
        sanitize();
    }

    public boolean save(Path path) {
        sanitize();
        try {
            Files.createDirectories(path.getParent());
            Files.writeString(path, GSON.toJson(this) + "\n", StandardCharsets.UTF_8);
            return true;
        } catch (IOException exception) {
            RedstoneNumbersClient.LOGGER.warn("Cannot save redstonenumbers.json", exception);
            return false;
        }
    }
}
