import { mount } from 'cypress/vue';

type MountParams = Parameters<typeof mount>;
type OptionsParam = MountParams[1];

declare global {
  namespace Cypress {
    interface Chainable {
      mount: typeof mount;

      signJWT(enableAuth: boolean, permissions?: string[]): Promise<string>;
      getTestSelector(testSelector: string): Chainable<JQuery<Node>>;
      findTestSelector(testSelector: string): Chainable<JQuery<Node>>;
    }
  }
}
