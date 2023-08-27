import { z } from 'zod';
import { IngredientBaseSchema } from './ingredient';

export const RecipeBaseSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export const RecipeSchema = RecipeBaseSchema.extend({
  ingredients: z.lazy(() => IngredientBaseSchema.array())
});

export const RecipesResponseSchema = z.object({
  page: z.number(),
  recipes: RecipeBaseSchema.array(),
  total: z.number()
});