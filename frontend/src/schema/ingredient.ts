import { RecipeBaseSchema } from '@/schema/recipe';
import { z } from 'zod';

export const IngredientBaseSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().nullable(),
  likes: z.number()
});

export const IngredientSchema = IngredientBaseSchema.extend({
  recipes: z.lazy(() => RecipeBaseSchema.array())
});

export const IngredientsResponseSchema = z.object({
  page: z.number(),
  ingredients: IngredientSchema.array(),
  total: z.number(),
  per_page: z.number()
});

export const IngredientCreateSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export const IngredientUpdateSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().url().nullable()
});

export const IngredientCreatedResponseSchema = z.object({
  id: z.number()
});

export const IngredientUpdatedResponseSchema = IngredientSchema.extend({});
export const IngredientDeletedResponseSchema = z.object({
  id: z.number()
});

export const IngredientLikedResponseSchema = z.object({
  id: z.number(),
  total_likes: z.number()
});

export type IngredientBase = z.infer<typeof IngredientBaseSchema>;
export type Ingredient = z.infer<typeof IngredientSchema>;

export type IngredientCreate = z.infer<typeof IngredientCreateSchema>;
export type IngredientUpdate = z.infer<typeof IngredientUpdateSchema>;

export type IngredientsResponse = z.infer<typeof IngredientsResponseSchema>;
export type IngredientCreatedResponse = z.infer<typeof IngredientCreatedResponseSchema>;
export type IngredientUpdatedResponse = z.infer<typeof IngredientUpdatedResponseSchema>;
export type IngredientDeletedResponse = z.infer<typeof IngredientDeletedResponseSchema>;

export type IngredientLikedResponse = z.infer<typeof IngredientLikedResponseSchema>;
