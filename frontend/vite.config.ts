import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
    plugins: [
        VitePWA({
            registerType: "autoUpdate",
            devOptions: {
                enabled: true,
            },
            includeAssets: ["favicon.ico", "icon.png", "robots.txt"],
            injectRegister: "auto",
            manifest: {
                name: "My Awesome App",
                short_name: "MyApp",
                description: "My Awesome App description",
                theme_color: "#ffffff",
                icons: [
                    {
                        src: "/favicon.ico",
                        sizes: "64x64 32x32 24x24 16x16",
                        type: "image/x-icon",
                    },
                    {
                        src: "/icon.png",
                        sizes: "512x512",
                        type: "image/png",
                        purpose: "any maskable",
                    },
                ],
            },
        }),
    ],
});
