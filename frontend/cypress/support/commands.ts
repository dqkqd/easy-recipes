/// <reference types="cypress" />
// ***********************************************
// This example commands.ts shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
//
// declare global {
//   namespace Cypress {
//     interface Chainable {
//       login(email: string, password: string): Chainable<void>
//       drag(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       dismiss(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       visit(originalFn: CommandOriginalFn, url: string, options: Partial<VisitOptions>): Chainable<Element>
//     }
//   }
// }

import * as jose from 'jose';
import auth0 from '../../src/plugins/auth0';

declare global {
  namespace Cypress {
    interface Chainable {
      signJWT(enableAuth: boolean, permissions?: string[]): Promise<string>;
      getTestSelector(testSelector: string): Chainable<JQuery<Node>>;
      findTestSelector(subject: any, testSelector: string): Chainable<JQuery<Node>>;
    }
  }
}

Cypress.Commands.add('signJWT', async (enableAuth: boolean, permissions: string[] = []) => {
  const keyPair = await window.crypto.subtle.generateKey(
    {
      name: 'RSASSA-PKCS1-v1_5',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256'
    },
    true,
    ['sign', 'verify']
  );
  const jwt = await new jose.SignJWT({ permissions: permissions })
    .setProtectedHeader({ alg: 'RS256' })
    .sign(keyPair.privateKey);
  auth0.isAuthenticated.value = enableAuth;
  cy.stub(auth0, 'getAccessTokenSilently').resolves(jwt);

  return jwt;
});

Cypress.Commands.add('getTestSelector', (testSelector: string) => {
  return cy.get(`[data-test=${testSelector}]`);
});

Cypress.Commands.add('findTestSelector', { prevSubject: true }, (subject, testSelector: string) => {
  return subject.find(`[data-test=${testSelector}]`);
});
