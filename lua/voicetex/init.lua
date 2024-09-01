local M = {}

function M.setup(opts)
  opts = opts or {}
  local stop_key = opts.stop_key and #opts.stop_key > 0 and opts.stop_key or ''
  
  -- Check if the function exists
  if vim.fn.exists('*VoiceTexSetup') == 1 then
    local result = vim.fn.VoiceTexSetup(stop_key)
    if result ~= "Setup complete" then
      vim.api.nvim_err_writeln("VoiceTexSetup failed: " .. tostring(result))
    end
  else
    vim.api.nvim_err_writeln("VoiceTexSetup function not found. Make sure the plugin is properly loaded.")
  end
end

return M
