package dev.tqnl.redstonenumbers;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** The small user-editable configuration, loaded once when the client starts. */
public final class ModConfig {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    public boolean enabled = true;
    public int range = 32;
    public int maxLabels = 8192;
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

    public void save(Path path) {
        sanitize();
        try {
            Files.createDirectories(path.getParent());
            Files.writeString(path, GSON.toJson(this) + "\n", StandardCharsets.UTF_8);
        } catch (IOException exception) {
            RedstoneNumbersClient.LOGGER.warn("Cannot save redstonenumbers.json", exception);
        }
    }
}
