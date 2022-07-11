module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    plugins: [
        "@typescript-eslint",
        "@microsoft/sdl",
        "security"
    ],
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:security/recommended'
    ],
};