<template>
  <div class="not-found min-h-screen bg-[#050810] flex items-center justify-center">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid"></div>

    <div class="relative z-20 text-center px-8">
      <!-- 雷达失败动画 -->
      <div class="radar-fail w-[260px] h-[260px] mx-auto mb-8 relative">
        <div class="w-full h-full rounded-full border border-neon-green/20 relative radar-bg">
          <div class="radar-lines"></div>
          <div class="sweep-fail absolute inset-0 rounded-full"></div>
        </div>
      </div>

      <!-- 404 代码 -->
      <div class="code font-rajdhani text-[80px] font-bold text-[#ff4d4d] leading-none tracking-[4px] mb-4">
        404
      </div>

      <!-- 标签 -->
      <div class="label font-mono text-xs text-neon-green tracking-[2px] mb-6">
        // SIGNAL.LOST // 信号未捕获
      </div>

      <!-- 波形图 -->
      <svg class="wave mx-auto mb-6 opacity-50" width="180" height="24" viewBox="0 0 180 24" preserveAspectRatio="none">
        <polyline
          fill="none"
          stroke="#00ffc8"
          stroke-width="1"
          points="0,12 10,12 15,4 20,20 25,12 35,12 40,8 45,16 50,12 70,12 75,2 80,22 85,12 110,12 115,9 120,15 125,12 180,12"
          opacity="0.6"
        />
      </svg>

      <!-- 描述 -->
      <p class="desc text-sm text-text-dim leading-relaxed max-w-[300px] mx-auto mb-8">
        雷达扫描失败。<br>
        你访问的坐标不存在于当前频段。
      </p>

      <!-- 返回按钮 -->
      <button
        @click="$router.push('/')"
        class="btn font-mono text-sm bg-neon-green text-[#050810] px-8 py-3 font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow"
        style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
      >
        ← 返回主信号
      </button>
    </div>
  </div>
</template>

<script setup>
// 404 页面
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(rgba(0,255,200,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,200,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

.radar-bg {
  background:
    radial-gradient(circle, transparent 18%, rgba(0,255,200,0.03) 19%, transparent 20%,
                    transparent 38%, rgba(0,255,200,0.03) 39%, transparent 40%,
                    transparent 58%, rgba(0,255,200,0.03) 59%, transparent 60%);
  box-shadow: inset 0 0 40px rgba(0,255,200,0.05);
}

.radar-lines::before,
.radar-lines::after {
  content: '';
  position: absolute;
  background: rgba(0,255,200,0.15);
}

.radar-lines::before {
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
}

.radar-lines::after {
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
}

.sweep-fail {
  background: conic-gradient(from 135deg, rgba(255, 77, 77, 0.4), transparent 30deg);
  animation: sweep-stuck 0.5s ease-in-out infinite;
  transform: rotate(135deg);
  border-radius: 50%;
}

@keyframes sweep-stuck {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
</style>
