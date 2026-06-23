import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const inspirations = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/inspirations' }),
  schema: z.object({
    title: z.string(),
    image: z.string(),                    // 图片路径，如 /images/inspirations/xxx.jpg
    style: z.string(),
    colorScheme: z.string(),
    layout: z.string(),
    note: z.string().optional(),          // 备注，可选
    source: z.string().optional(),        // 来源链接，可选
    createdAt: z.coerce.date(),         // 创建时间，自动生成
  }),
});

export const collections = { inspirations };
