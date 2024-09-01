local M = {}

function M.setup(opts)
  opts = opts or {}
  local stop_key = opts.stop_key and #opts.stop_key > 0 and opts.stop_key or ''
  vim.cmd('VoiceTexSetup ' .. stop_key)
end

return M
