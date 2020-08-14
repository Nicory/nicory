module.exports = (cb, ms) => {
  return new Promise((resolve, reject) => {
	  cb();
    setTimeout(() => reject("Execution took too long"), ms);
  });
};