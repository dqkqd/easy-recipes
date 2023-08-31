import { z } from 'zod';
import { RecipeBaseSchema } from './recipe';

export const IngredientBaseSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
  image_uri: z.string().nullable()
});

export const IngredientSchema = IngredientBaseSchema.extend({
  recipes: z.lazy(() => RecipeBaseSchema.array())
});

export type IngredientBase = z.infer<typeof IngredientBaseSchema>;
export type Ingredient = z.infer<typeof IngredientSchema>;
