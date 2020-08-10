const twig = require('twig');

module.exports = async (tpl, ctx) => {
	return await twig.twig({
		data: tpl,
		load: () => ""
	}).renderAsync(ctx);
};