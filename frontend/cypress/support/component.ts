import { VApp } from 'vuetify/components';
// ***********************************************************
import vuetify from '../../src/plugins/vuetify';

// This example support/component.ts is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

import { createTestingPinia } from '@pinia/testing';
import { mount } from 'cypress/vue';
import { h } from 'vue';
import router from '../../src/router';

// Augment the Cypress namespace to include type definitions for
// your custom command.
// Alternatively, can be defined in cypress/support/component.d.ts
// with a <reference path="./component" /> at the top of your spec.
declare global {
  namespace Cypress {
    interface Chainable {
      mount: typeof mount;
    }
  }
}

// @ts-ignore
Cypress.Commands.add('mount', (component, options = {}) => {
  // Setup options object
  options.global = options.global || {};
  options.global.stubs = options.global.stubs || {};
  options.global.stubs['transition'] = false;
  options.global.components = options.global.components || {};
  options.global.plugins = options.global.plugins || [];

  /* Add any global plugins */
  options.global.plugins.push({
    install(app) {
      app.use(vuetify); //import vuetify from you vuetify config
    }
  });

  // Add router plugin
  options.global.plugins.push({
    install(app) {
      app.use(router);
    }
  });

  options.global.plugins.push({
    install(app) {
      app.use(
        createTestingPinia({
          createSpy: cy.spy
        })
      );
    }
  });

  return mount(() => h(VApp, {}, component), options);
});

// Example use:
// cy.mount(MyComponent)
