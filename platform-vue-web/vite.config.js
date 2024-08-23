import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import WindiCSS from 'vite-plugin-windicss';

// export 引用出去，这里的配置在整个项目中生效。
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd());

  return {
    resolve: {
      // alias 设置别名，可以自定义
      // 当前文件名，下面的 src.
      // 其实按照相对路径来理解，当前项目下的 src 文件夹。
      alias: {
        "~": path.resolve(__dirname, "src")
      }
    },
    plugins: [
      // 安装插件之后放这里
      vue(),
      WindiCSS(),
    ],
    // 前端跨域处理逻辑
    server: {
      proxy: {
        "/api": {
          target:'http://127.0.0.1:5000',
          // 通过上面env 引用对应的变量
          // target: env.VITE_APP_API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },

  };
});