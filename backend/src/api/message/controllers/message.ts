/**
 * message controller
 */

import { factories } from '@strapi/strapi'

export default factories.createCoreController('api::message.message', ({ strapi }) => ({
  // Endpoint para enviar mensagem
  async sendMessage(ctx) {
    const { chatId, content, message_type = 'text', widget_type, widget_config } = ctx.request.body;
    const userId = ctx.state.user.id;

    try {
      // Verificar se o usuário está no chat
      const chat = await strapi.entityService.findOne('api::chat.chat', chatId, {
        populate: ['participants']
      });

      if (!chat) {
        return ctx.badRequest('Chat not found');
      }

      const userInChat = chat.participants?.some((participant: any) => participant.id === userId);
      if (!userInChat) {
        return ctx.forbidden('User not in chat');
      }

      // Criar mensagem
      const message = await strapi.entityService.create('api::message.message', {
        data: {
          content,
          message_type,
          sender: userId,
          chat: chatId,
          widget_type,
          widget_config
        },
        populate: ['sender', 'chat']
      });

      // Atualizar último horário de mensagem do chat
      await strapi.entityService.update('api::chat.chat', chatId, {
        data: { last_message_at: new Date() }
      });

      return ctx.send({ message });
    } catch (error) {
      ctx.throw(500, error);
    }
  },

  // Endpoint para marcar mensagem como lida
  async markAsRead(ctx) {
    const { id } = ctx.params;
    const userId = ctx.state.user.id;

    try {
      const message = await strapi.entityService.findOne('api::message.message', id, {
        populate: ['chat.participants']
      });

      if (!message) {
        return ctx.notFound('Message not found');
      }

      // Verificar se o usuário está no chat
      const userInChat = message.chat.participants?.some((participant: any) => participant.id === userId);
      if (!userInChat) {
        return ctx.forbidden('User not in chat');
      }

      // Não pode marcar própria mensagem como lida
      if (message.sender?.id === userId) {
        return ctx.badRequest('Cannot mark own message as read');
      }

      const updatedMessage = await strapi.entityService.update('api::message.message', id, {
        data: { read_at: new Date() }
      });

      return ctx.send({ message: updatedMessage });
    } catch (error) {
      ctx.throw(500, error);
    }
  }
}));
