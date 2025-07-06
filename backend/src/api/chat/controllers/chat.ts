/**
 * chat controller
 */

import { factories } from '@strapi/strapi'

export default factories.createCoreController('api::chat.chat', ({ strapi }) => ({
  // Endpoint customizado: POST /api/chats/join-group-chat
  async joinGroupChat(ctx) {
    const { groupId } = ctx.request.body;
    const userId = ctx.state.user.id;

    try {
      // Verificar se o usuário está no grupo
      const group = await strapi.entityService.findOne('api::group.group', groupId, {
        populate: ['users']
      });

      if (!group) {
        return ctx.badRequest('Group not found');
      }

      const userInGroup = group.users?.some((user: any) => user.id === userId);
      if (!userInGroup) {
        return ctx.forbidden('User not in group');
      }

      // Buscar ou criar chat do grupo
      let chatResults = await strapi.entityService.findMany('api::chat.chat', {
        filters: { group: { id: groupId } },
        populate: ['participants']
      });

      let chat;
      if (chatResults.length === 0) {
        // Criar novo chat para o grupo
        chat = await strapi.entityService.create('api::chat.chat', {
          data: {
            name: group.name,
            chat_type: 'group',
            group: groupId,
            participants: group.users?.map((user: any) => user.id) || [],
            is_active: true
          }
        });
      } else {
        chat = chatResults[0];
      }

      return ctx.send({ chat });
    } catch (error) {
      ctx.throw(500, error);
    }
  },

  // Endpoint customizado: GET /api/chats/my-chats
  async getMyChats(ctx) {
    const userId = ctx.state.user.id;

    try {
      const chats = await strapi.entityService.findMany('api::chat.chat', {
        filters: {
          participants: { id: userId }
        },
        populate: ['participants', 'group', 'messages'],
        sort: { last_message_at: 'desc' }
      });

      return ctx.send({ chats });
    } catch (error) {
      ctx.throw(500, error);
    }
  }
}));