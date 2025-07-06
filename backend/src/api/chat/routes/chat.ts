/**
 * chat router
 */

import { factories } from '@strapi/strapi';

export default {
  routes: [
    // Rotas padrão do Strapi
    ...factories.createCoreRouter('api::chat.chat').routes,
    
    // Rotas customizadas
    {
      method: 'POST',
      path: '/chats/join-group-chat',
      handler: 'chat.joinGroupChat',
      config: {
        policies: [],
        middlewares: [],
      },
    },
    {
      method: 'GET',
      path: '/chats/my-chats',
      handler: 'chat.getMyChats',
      config: {
        policies: [],
        middlewares: [],
      },
    },
  ],
};