import { defineConfig, presetIcons, presetUno, presetWebFonts, transformerDirectives, transformerVariantGroup } from 'unocss'

export default defineConfig({
    presets: [
        presetUno(),
        presetIcons(),
        presetWebFonts({
            provider: 'google',
            fonts: {
                sans: 'IBM Plex Sans JP',
            },
        }),
    ],

    theme: {
        colors: {
            fprimary: '#333',
            fsecondary: '#666',
            fwhite: '#f0f0f0',
            spotify: '#1DB954',
            spotifydark: '#195424',

            entryBack: '#1118',
            entryBorder: '#aaa',
            buttonBack: '#1118',
            buttonBackHover: '#1115',
            buttonBorder: '#aaa',
            buttonOrange: '#e50',
            buttonOrangeHover: '#d40',

            pressButtonBorder: '#0a0',
            pressButtonBorderHover: '#0ac',
            pressSubButtonBorder: '#80c',
            pressSubButtonBorderHover: '#05c',

            windowBack: '#1113',
        },
    },

    transformers: [
        transformerDirectives(),
        transformerVariantGroup(),
    ],
})