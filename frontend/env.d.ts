/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // 使用 object 代替 {}，虽然 any 还是可能会被警告，但通常 object 能解决大部分红线
  const component: DefineComponent<object, object, any>
  export default component
}
