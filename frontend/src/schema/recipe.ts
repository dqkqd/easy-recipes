import { z } from 'zod';

export const recipeSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string(),
  image_uri: z.string().nullable(),
  ingredients: z.string().array()
});

export const getRecipeSchema = z.object({
  page: z.number(),
  recipes: z.array(recipeSchema),
  total: z.number()
});

export type RecipesResponse = z.infer<typeof getRecipeSchema>;
