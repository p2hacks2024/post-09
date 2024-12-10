import { defineConfig, presetUno, presetWebFonts, transformerDirectives, transformerVariantGroup } from 'unocss'

export default defineConfig({
    presets: [
        presetUno(),
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
        },
    },

    transformers: [
        transformerDirectives(),
        transformerVariantGroup(),
    ],
})