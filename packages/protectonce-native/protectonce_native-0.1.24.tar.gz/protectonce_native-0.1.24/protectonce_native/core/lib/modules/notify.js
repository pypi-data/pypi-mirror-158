const Logger = require('../utils/logger');
const HeartbeatCache = require('../reports/heartbeat_cache');

function notify(key, ...args) {
  try {
    if (key === 'BOM.usedModule') {
      HeartbeatCache.cacheDynamicBom(args[0]);
    }
  } catch (e) {
    Logger.write(Logger.ERROR && `Error in notify method : ${e}`);
  }

}
module.exports = notify