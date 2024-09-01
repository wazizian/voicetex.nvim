local M = {}

function M.setup(opts)
  opts = opts or {}
  vim.cmd('VoiceTexSetup ' .. (opts.stop_key or ''))
end

return M
