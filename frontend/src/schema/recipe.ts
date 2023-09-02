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
  recipes: RecipeSchema.array(),
  total: z.number(),
  per_page: z.number()
});

export const RecipeCreatedResponseSchema = z.object({
  id: z.number()
});

export const RecipeDeletedResponseSchema = z.object({
  id: z.number()
});

export const RecipeCreateSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export type RecipeBase = z.infer<typeof RecipeBaseSchema>;
export type Recipe = z.infer<typeof RecipeSchema>;
export type RecipesResponse = z.infer<typeof RecipesResponseSchema>;
export type RecipeCreatedResponse = z.infer<typeof RecipeCreatedResponseSchema>;
export type RecipeCreate = z.infer<typeof RecipeCreateSchema>;

export type RecipeDeletedResponse = z.infer<typeof RecipeDeletedResponseSchema>;
