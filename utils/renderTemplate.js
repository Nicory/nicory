const twig = require('twig');

module.exports = (tpl, ctx) => {
	return twig.twig({
		data: tpl,
	}).render(ctx);
};