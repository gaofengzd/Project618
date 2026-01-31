import { globalIgnores } from 'eslint/config'
import { defineConfigWithVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import pluginVue from 'eslint-plugin-vue'
import skipFormatting from 'eslint-config-prettier/flat'
import pluginOxlint from 'eslint-plugin-oxlint'

// To allow more languages other than `ts` in `.vue` files, uncomment the following lines:
// import { configureVueProject } from '@vue/eslint-config-typescript'
// configureVueProject({ scriptLangs: ['ts', 'tsx'] })
// More info at https://github.com/vuejs/eslint-config-typescript/#advanced-setup

export default defineConfigWithVueTs(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{vue,ts,mts,tsx}'],
  },
  {
    name: 'app/variable-rules',
    // 在这里添加 rules 对象
    rules: {
      // 关闭 "禁止使用 any" 的规则
      '@typescript-eslint/no-explicit-any': 'off',

      // 关闭 "禁止使用特定类型" (如 {}) 的规则
      '@typescript-eslint/ban-types': 'off',

      // 关闭 "组件名必须多单词" 的规则 (Vue常见报错)
      'vue/multi-word-component-names': 'off',

      // 如果有未使用的变量报错，可以改为警告 'warn' 或者关闭 'off'
      '@typescript-eslint/no-unused-vars': 'warn',
    }
  },

  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  ...pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,

  skipFormatting,

  ...pluginOxlint.configs['flat/recommended'],
)
