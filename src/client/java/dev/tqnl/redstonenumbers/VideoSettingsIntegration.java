package dev.tqnl.redstonenumbers;

import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.WeakHashMap;
import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.fabric.api.client.screen.v1.ScreenKeyboardEvents;
import net.fabricmc.fabric.api.client.screen.v1.ScreenMouseEvents;
import net.fabricmc.fabric.api.client.screen.v1.Screens;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.AbstractWidget;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.navigation.ScreenRectangle;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.options.VideoSettingsScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.contents.TranslatableContents;

/** A GUI-only shortcut for vanilla and replacement video screens, using Fabric screen events. */
public final class VideoSettingsIntegration {
    private static final String BUTTON_KEY = "screen.redstonenumbers.video_button";
    private static final Set<Screen> VIDEO_SCREENS = Collections.newSetFromMap(new WeakHashMap<>());
    private static Screen videoLauncher;

    private VideoSettingsIntegration() { }

    public static void register() {
        ScreenEvents.AFTER_INIT.register((client, screen, width, height) -> {
            boolean fromVideoButton = videoLauncher != null && videoLauncher != screen;
            if (fromVideoButton) videoLauncher = null;
            watchVideoLauncher(screen);
            if (hasSodiumSettings(screen)) return;
            if (screen instanceof VideoSettingsScreen || translation(screen.getTitle(), "options.videoTitle")
                    || VIDEO_SCREENS.contains(screen) || fromVideoButton) {
                VIDEO_SCREENS.add(screen);
                addShortcut(client, screen);
            }
        });
    }

    private static void watchVideoLauncher(Screen screen) {
        List<AbstractWidget> buttons = Screens.getWidgets(screen);
        if (buttons.stream().noneMatch(VideoSettingsIntegration::videoEntry)) return;
        // Observe an actual Video Settings activation rather than guessing arbitrary mod screen names.
        ScreenMouseEvents.beforeMouseClick(screen).register((source, event) -> {
            if (event.button() == 0 && Screens.getWidgets(source).stream()
                    .anyMatch(widget -> videoEntry(widget) && widget.active && widget.visible
                            && widget.isMouseOver(event.x(), event.y()))) {
                videoLauncher = source;
            }
        });
        ScreenMouseEvents.afterMouseClick(screen).register((source, event, consumed) -> {
            videoLauncher = null;
            return consumed;
        });
        ScreenKeyboardEvents.beforeKeyPress(screen).register((source, event) -> {
            if (event.isSelection() && source.getFocused() instanceof AbstractWidget widget
                    && videoEntry(widget) && widget.active && widget.visible) {
                videoLauncher = source;
            }
        });
        ScreenKeyboardEvents.afterKeyPress(screen).register((source, event) -> videoLauncher = null);
    }

    private static boolean videoEntry(AbstractWidget widget) {
        return translation(widget.getMessage(), "options.video");
    }

    private static boolean hasSodiumSettings(Screen screen) {
        // Sodium and Reese's independent replacement both expose the supported config-entry API.
        for (Class<?> type = screen.getClass(); type != null; type = type.getSuperclass()) {
            if (type.getName().equals("net.caffeinemc.mods.sodium.client.gui.VideoSettingsScreen")
                    || type.getName().equals("me.flashyreese.mods.reeses_sodium_options.client.gui.SodiumVideoOptionsScreen")) return true;
        }
        return false;
    }

    private static boolean translation(Component component, String key) {
        return component.getContents() instanceof TranslatableContents contents && contents.getKey().equals(key);
    }

    private static void addShortcut(Minecraft client, Screen screen) {
        List<AbstractWidget> buttons = Screens.getWidgets(screen);
        if (buttons.stream().anyMatch(widget -> translation(widget.getMessage(), BUTTON_KEY))) return;
        ScreenRectangle place = findSpace(client, screen, buttons);
        if (place == null) return;
        Component tooltip = Component.translatable("screen.redstonenumbers.video_button.tooltip");
        Button shortcut = Button.builder(Component.translatable(BUTTON_KEY),
                        button -> client.setScreen(RedstoneNumbersClient.createSettingsScreen(screen)))
                .bounds(place.left(), place.top(), 20, 20)
                .tooltip(Tooltip.create(tooltip))
                .createNarration(message -> tooltip.copy())
                .build();
        buttons.add(shortcut);
        // Some replacement screens draw their own widgets without calling Screen.render().
        // Drawing this small native control after that GUI also makes it visible there.
        ScreenEvents.afterExtract(screen).register((current, graphics, mouseX, mouseY, delta) ->
                shortcut.extractRenderState(graphics, mouseX, mouseY, delta));
        ScreenMouseEvents.allowMouseClick(screen).register((current, event) -> {
            if (event.button() == 0 && shortcut.isMouseOver(event.x(), event.y())) {
                shortcut.mouseClicked(event, false);
                return false;
            }
            return true;
        });
        ScreenKeyboardEvents.allowKeyPress(screen).register((current, event) -> {
            if (current.getFocused() == shortcut && event.isSelection()) {
                shortcut.keyPressed(event);
                return false;
            }
            return true;
        });
    }

    private static ScreenRectangle findSpace(Minecraft client, Screen screen, List<AbstractWidget> widgets) {
        int titleWidth = client.font.width(screen.getTitle());
        ScreenRectangle title = new ScreenRectangle((screen.width - titleWidth) / 2, 4, titleWidth, 20);
        for (int y : new int[]{screen.height - 24, 4}) {
            for (int x = 4; x <= screen.width - 24; x += 24) {
                ScreenRectangle candidate = new ScreenRectangle(x - 2, y - 2, 24, 24);
                if (y == 4 && candidate.intersects(title)) continue;
                boolean occupied = widgets.stream().anyMatch(widget -> widget.visible && candidate.intersects(
                        new ScreenRectangle(widget.getX(), widget.getY(), widget.getWidth(), widget.getHeight())));
                if (!occupied) return new ScreenRectangle(x, y, 20, 20);
            }
        }
        return null;
    }
}
