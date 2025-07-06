/**
 * message router
 */

import { factories } from '@strapi/strapi';

export default {
  routes: [
    // Rotas padrão do Strapi
    ...factories.createCoreRouter('api::message.message').routes,
    
    // Rotas customizadas
    {
      method: 'POST',
      path: '/messages/send',
      handler: 'message.sendMessage',
      config: {
        policies: [],
        middlewares: [],
      },
    },
    {
      method: 'PUT',
      path: '/messages/:id/read',
      handler: 'message.markAsRead',
      config: {
        policies: [],
        middlewares: [],
      },
    },
  ],
};