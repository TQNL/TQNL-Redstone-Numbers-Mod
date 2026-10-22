package dev.tqnl.redstonenumbers;

import java.nio.file.Path;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.CycleButton;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;

/** A small native form. Valid edits preview immediately; closing without Done restores them. */
public final class SettingsScreen extends Screen {
    private final Screen parent;
    private final ModConfig config;
    private final ModConfig original;
    private final Path path;
    private EditBox range;
    private EditBox limit;
    private EditBox scale;
    private Button done;
    private int left;
    private int top;
    private boolean accepted;
    private boolean valid = true;
    private boolean saveFailed;

    public SettingsScreen(Screen parent, ModConfig config, Path path) {
        super(Component.translatable("screen.redstonenumbers.title"));
        this.parent = parent;
        this.config = config;
        this.original = config.copy();
        this.path = path;
    }

    @Override
    protected void init() {
        left = width / 2 - 150;
        top = Math.max(42, height / 2 - 77);
        addRenderableWidget(CycleButton.onOffBuilder(config.enabled)
                .withTooltip(value -> Tooltip.create(Component.translatable("screen.redstonenumbers.enabled.help")))
                .create(left, top, 300, 20, Component.translatable("screen.redstonenumbers.enabled"),
                        (button, value) -> config.enabled = value));
        range = numberBox("range", Integer.toString(config.range), top + 28);
        limit = numberBox("limit", Integer.toString(config.maxLabels), top + 56);
        scale = numberBox("scale", Float.toString(config.scale), top + 84);
        done = addRenderableWidget(Button.builder(CommonComponents.GUI_DONE, button -> {
            if (config.save(path)) {
                accepted = true;
                minecraft.gui.setScreen(parent);
            } else {
                saveFailed = true;
            }
        }).bounds(left, top + 146, 96, 20).build());
        addRenderableWidget(Button.builder(CommonComponents.GUI_CANCEL, button -> onClose())
                .bounds(left + 102, top + 146, 96, 20).build());
        addRenderableWidget(Button.builder(Component.translatable("screen.redstonenumbers.reset"), button -> {
            config.copyFrom(new ModConfig());
            saveFailed = false;
            rebuildWidgets();
        }).bounds(left + 204, top + 146, 96, 20)
                .tooltip(Tooltip.create(Component.translatable("screen.redstonenumbers.reset.help"))).build());
        range.setResponder(value -> preview());
        limit.setResponder(value -> preview());
        scale.setResponder(value -> preview());
        preview();
    }

    private EditBox numberBox(String name, String value, int y) {
        EditBox box = new EditBox(font, left + 202, y, 98, 20,
                Component.translatable("screen.redstonenumbers." + name));
        box.setMaxLength(8);
        box.setValue(value);
        box.setTooltip(Tooltip.create(Component.translatable("screen.redstonenumbers." + name + ".help")));
        return addRenderableWidget(box);
    }

    private void preview() {
        Integer newRange = integer(range, 1, 128);
        Integer newLimit = integer(limit, 1, 65536);
        Float newScale = decimal(scale, 0.25F, 4.0F);
        valid = newRange != null && newLimit != null && newScale != null;
        done.active = valid;
        if (newRange != null) config.range = newRange;
        if (newLimit != null) config.maxLabels = newLimit;
        if (newScale != null) config.scale = newScale;
        saveFailed = false;
    }

    private static Integer integer(EditBox box, int min, int max) {
        try {
            int value = Integer.parseInt(box.getValue().trim());
            if (value >= min && value <= max) {
                box.setTextColor(0xFFFFFFFF);
                return value;
            }
        } catch (NumberFormatException ignored) { }
        box.setTextColor(0xFFFF7777);
        return null;
    }

    private static Float decimal(EditBox box, float min, float max) {
        try {
            float value = Float.parseFloat(box.getValue().trim());
            if (Float.isFinite(value) && value >= min && value <= max) {
                box.setTextColor(0xFFFFFFFF);
                return value;
            }
        } catch (NumberFormatException ignored) { }
        box.setTextColor(0xFFFF7777);
        return null;
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        graphics.centeredText(font, title, width / 2, top - 30, 0xFFFFFFFF);
        graphics.text(font, Component.translatable("screen.redstonenumbers.range"), left, top + 34, 0xFFFFFFFF);
        graphics.text(font, Component.translatable("screen.redstonenumbers.limit"), left, top + 62, 0xFFFFFFFF);
        graphics.text(font, Component.translatable("screen.redstonenumbers.scale"), left, top + 90, 0xFFFFFFFF);
        Component status = Component.translatable(saveFailed ? "screen.redstonenumbers.save_error"
                : valid ? "screen.redstonenumbers.preview" : "screen.redstonenumbers.invalid");
        graphics.textWithWordWrap(font, status, left, top + 114, 300,
                saveFailed || !valid ? 0xFFFF9999 : 0xFFBBBBBB);
    }

    @Override
    public void onClose() {
        config.copyFrom(original);
        minecraft.gui.setScreen(parent);
    }

    @Override
    public void removed() {
        if (!accepted) config.copyFrom(original);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
