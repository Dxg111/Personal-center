/**
 * 将逗号分隔的技术栈字符串解析为标签数组
 * 自动去除空白项，避免空字符串生成空标签
 */
export const getTechTags = (techStack) => {
  if (!techStack) return []

  return techStack
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean)
}
