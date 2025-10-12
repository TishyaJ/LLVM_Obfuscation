/**
 * @file config_parser.h
 * @brief Configuration Parser Header
 * 
 * Header for configuration parsing and management
 * of obfuscation settings.
 */

#ifndef CONFIG_PARSER_H
#define CONFIG_PARSER_H

#include <string>
#include <map>

namespace obfuscator {

/**
 * @class ConfigParser
 * @brief Configuration parser for obfuscation settings
 */
class ConfigParser {
private:
    std::map<std::string, std::string> config_;
    
public:
    /**
     * @brief Constructor
     */
    ConfigParser() = default;
    
    /**
     * @brief Load configuration from file
     * @param filename Configuration file path
     * @return true if loaded successfully
     */
    bool loadFromFile(const std::string &filename);
    
    /**
     * @brief Get configuration value
     * @param key Configuration key
     * @param defaultValue Default value if key not found
     * @return Configuration value
     */
    std::string getValue(const std::string &key, const std::string &defaultValue = "");
    
    /**
     * @brief Set configuration value
     * @param key Configuration key
     * @param value Configuration value
     */
    void setValue(const std::string &key, const std::string &value);
    
    /**
     * @brief Check if a pass is enabled
     * @param passName Name of the pass
     * @return true if pass is enabled
     */
    bool isPassEnabled(const std::string &passName);
    
    /**
     * @brief Get pass configuration
     * @param passName Name of the pass
     * @return Map of pass configuration
     */
    std::map<std::string, std::string> getPassConfig(const std::string &passName);
};

} // namespace obfuscator

#endif // CONFIG_PARSER_H
