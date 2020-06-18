'use strict';
const path = require('path');
const config = require('../config');
const packageConfig = require('../package.json');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

exports.assetsPath = function (_path) {
    const assetsSubDirectory = process.env.NODE_ENV === 'production'
        ? config.build.assetsSubDirectory
        : config.dev.assetsSubDirectory;

    return path.posix.join(assetsSubDirectory, _path);
};

exports.cssLoaders = function (options) {
    return {
        css: [
            process.env.NODE_ENV !== 'production'
                ? 'vue-style-loader'
                : MiniCssExtractPlugin.loader,
            'css-loader'
        ]
    };
}

// Generate loaders for standalone style files (outside of .vue)
exports.styleLoaders = function (options) {
    const output = []
    const loaders = exports.cssLoaders(options)
    for (const extension in loaders) {
        output.push({
            test: new RegExp('\\.' + extension + '$'),
            use: loaders[extension],
        });
    }
    return output;
};

exports.createNotifierCallback = () => {
    const notifier = require('node-notifier');

    return (severity, errors) => {
        if (severity !== 'error') return;

        const error = errors[0];
        const filename = error.file && error.file.split('!')
            .pop();

        notifier.notify({
            title: packageConfig.name,
            message: severity + ': ' + error.name,
            subtitle: filename || '',
            icon: path.join(__dirname, 'logo.png')
        });
    };
};
