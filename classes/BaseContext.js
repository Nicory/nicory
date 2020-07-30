/**
 * Интерфейс для базового контекста
 * 
 * @interface
 */
class BaseContext {
  constructor() { }
  /**
   * Получение контекста
   *
   * @async
   * @returns {Promise<Object<string, any>>}
   */
  async getContext() { }
}

module.exports = BaseContext;