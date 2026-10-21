package dev.tqnl.redstonenumbers;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;

/** Loaded only when the optional Mod Menu mod asks for its entrypoint. */
public final class ModMenuIntegration implements ModMenuApi {
    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return RedstoneNumbersClient::createSettingsScreen;
    }
}
