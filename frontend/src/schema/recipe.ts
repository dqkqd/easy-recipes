import { IngredientBaseSchema } from '@/schema/ingredient';
import { z } from 'zod';

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

export const RecipeCreateSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export const RecipeUpdateSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export const RecipeCreatedResponseSchema = z.object({
  id: z.number()
});

export const RecipeUpdatedResponseSchema = RecipeSchema.extend({});
export const RecipeDeletedResponseSchema = z.object({
  id: z.number()
});

export type RecipeBase = z.infer<typeof RecipeBaseSchema>;
export type Recipe = z.infer<typeof RecipeSchema>;
export type RecipeCreate = z.infer<typeof RecipeCreateSchema>;
export type RecipeUpdate = z.infer<typeof RecipeUpdateSchema>;

export type RecipesResponse = z.infer<typeof RecipesResponseSchema>;
export type RecipeCreatedResponse = z.infer<typeof RecipeCreatedResponseSchema>;
export type RecipeUpdatedResponse = z.infer<typeof RecipeUpdatedResponseSchema>;
export type RecipeDeletedResponse = z.infer<typeof RecipeDeletedResponseSchema>;
