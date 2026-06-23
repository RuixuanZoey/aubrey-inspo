import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const inspirations = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/inspirations' }),
  schema: z.object({
    title: z.string(),
    image: z.string(),                    // 图片路径，如 /images/inspirations/xxx.jpg
    style: z.enum(['商业', '科技', '简约', '其他']),
    colorScheme: z.enum(['紫', '绿', '蓝', '橙', '黑灰', '其他']),
    layout: z.enum(['品牌墙', '图表', '数字高亮', '产品展示', '并列关系', '对比关系', '目录', '其他']),
    note: z.string().optional(),          // 备注，可选
    source: z.string().optional(),        // 来源链接，可选
    createdAt: z.coerce.date(),         // 创建时间，自动生成
  }),
});

export const collections = { inspirations };
