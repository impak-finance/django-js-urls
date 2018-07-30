window.reverse = (function () {
  const urls = {{ urls|safe }};
  const argRegex = /<\w*>/g;

  return function(name) {
    const urlPattern = urls[name];
    let url = urlPattern;

    if (!urlPattern) {
      throw "URL '" + name + "' not found";
    }

    if (arguments.length === 0) {
      return url;
    }

    if (typeof (arguments[1]) == 'object' && !Array.isArray(arguments[1])) {
      const tokens = urlPattern.match(argRegex);

      if (tokens) {
        for (let i=0; i < tokens.length; i += 1) {
          const token = tokens[i];
          const argName = token.slice(1, -1);
          const argValue = arguments[1][argName];

          if (argValue === undefined) {
            throw "Property '" + argName + "' not found";
          }
          url = url.replace(token, argValue);
        }
      }
    } else {
      const tokens = urlPattern.match(argRegex);

      if (tokens) {
        if (tokens.length !== arguments[1].length) {
          throw "Wrong number of argument";
        }

        for (let i=0; i < tokens.length; i += 1) {
          const token = tokens[i];
          const argValue = arguments[1][i];
          url = url.replace(token, argValue);
        }
      }
    }

    return url;
  };
})();