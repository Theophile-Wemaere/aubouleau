/** @type {import('tailwindcss').Config} */
module.exports = {
    corePlugins: {
        // Set this to `false` to disable tailwindcss default styling
        // See: https://tailwindcss.com/docs/preflight
        preflight: true
    },
    content: [
        // Templates directory
        './aubouleau_web/templates/**/*.html',
        // Flowbite
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin')({
            charts: true,
        }),
    ],
}
