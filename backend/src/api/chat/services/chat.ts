/**
 * chat service
 */

import { factories } from '@strapi/strapi';

export default factories.createCoreService('api::chat.chat', ({ strapi }) => ({
  // Lógica de negócio para criar chat direto entre usuários
  async createDirectChat(user1Id: number, user2Id: number) {
    // Verificar se já existe chat direto entre os usuários
    const existingChat = await strapi.entityService.findMany('api::chat.chat', {
      filters: {
        chat_type: 'direct',
        participants: {
          $and: [
            { id: user1Id },
            { id: user2Id }
          ]
        }
      },
      populate: ['participants']
    });

    if (existingChat.length > 0) {
      return existingChat[0];
    }

    // Criar novo chat direto
    const chat = await strapi.entityService.create('api::chat.chat', {
      data: {
        chat_type: 'direct',
        participants: [user1Id, user2Id],
        is_active: true
      }
    });

    return chat;
  },

  // Lógica para marcar mensagens como lidas
  async markMessagesAsRead(chatId: number, userId: number) {
    const messages = await strapi.entityService.findMany('api::message.message', {
      filters: {
        chat: { id: chatId },
        read_at: null,
        sender: { id: { $ne: userId } }
      }
    });

    // Marcar todas as mensagens não lidas como lidas
    const updatePromises = messages.map(message => 
      strapi.entityService.update('api::message.message', message.id, {
        data: { read_at: new Date() }
      })
    );

    await Promise.all(updatePromises);
    
    return messages.length;
  },

  // Lógica para buscar chats com contadores de mensagens não lidas
  async getChatsWithUnreadCount(userId: number) {
    const chats = await strapi.entityService.findMany('api::chat.chat', {
      filters: {
        participants: { id: userId }
      },
      populate: {
        participants: true,
        messages: {
          filters: {
            read_at: null,
            sender: { id: { $ne: userId } }
          }
        }
      },
      sort: { last_message_at: 'desc' }
    });

    // Adicionar contador de mensagens não lidas
    return chats.map(chat => ({
      ...chat,
      unread_count: chat.messages.length
    }));
  }
}));
