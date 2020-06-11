// https://eslint.org/docs/user-guide/configuring

module.exports = {
    root: true,
    parserOptions: {
        parser: 'babel-eslint'
    },
    env: {
        browser: true,
    },
    extends: ['plugin:vue/base', 'plugin:vue/essential', 'airbnb-base'],
    plugins: ['vue'],
    settings: {
        'import/resolver': {
            webpack: {
                config: 'build/webpack.base.conf.js'
            }
        }
    },
    rules: {
        'import/extensions': ['error', 'always', {
            js: 'never',
            vue: 'never'
        }],
        'indent': ['error', 4],
        // 'vue/script-indent': ['error', 4, { 'baseIndent': 1 }],
        'no-param-reassign': ['error', {
            props: true,
            ignorePropertyModificationsFor: [
                'state',
                'acc',
                'e'
            ]
        }],
        'import/no-extraneous-dependencies': ['error', {
            optionalDependencies: ['test/unit/index.js']
        }],
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
    },
    'overrides': [{
        'files': ['*.vue'],
        'rules': {
            'indent': 'off',
            'max-len': ['error', {
                'code': 120,
                'ignoreComments': true
            }],
            'object-curly-newline': ['error', {
                'ObjectExpression': { 'consistent': true }
            }]
        }
    }]
};
