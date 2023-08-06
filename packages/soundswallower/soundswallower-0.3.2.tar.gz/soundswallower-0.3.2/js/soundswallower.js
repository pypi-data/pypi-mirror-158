
var Module = (() => {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  if (typeof __filename !== 'undefined') _scriptDir = _scriptDir || __filename;
  return (
function(Module) {
  Module = Module || {};



// The Module object: Our interface to the outside world. We import
// and export values on it. There are various ways Module can be used:
// 1. Not defined. We create it here
// 2. A function parameter, function(Module) { ..generated code.. }
// 3. pre-run appended it, var Module = {}; ..generated code..
// 4. External script tag defines var Module.
// We need to check if Module already exists (e.g. case 3 above).
// Substitution will be replaced with actual code on later stage of the build,
// this way Closure Compiler will not mangle it (e.g. case 4. above).
// Note that if you want to run closure, and also to use Module
// after the generated code, you will need to define   var Module = {};
// before the code. Then that object will be used in the code, and you
// can continue to use Module afterwards as well.
var Module = typeof Module != 'undefined' ? Module : {};

// See https://caniuse.com/mdn-javascript_builtins_object_assign

// Set up the promise that indicates the Module is initialized
var readyPromiseResolve, readyPromiseReject;
Module['ready'] = new Promise(function(resolve, reject) {
  readyPromiseResolve = resolve;
  readyPromiseReject = reject;
});

// --pre-jses are emitted after the Module integration code, so that they can
// refer to Module (if they choose; they can also define Module)


// Sometimes an existing Module object exists with properties
// meant to overwrite the default module functionality. Here
// we collect those properties and reapply _after_ we configure
// the current environment's defaults to avoid having to be so
// defensive during initialization.
var moduleOverrides = Object.assign({}, Module);

var arguments_ = [];
var thisProgram = './this.program';
var quit_ = (status, toThrow) => {
  throw toThrow;
};

// Determine the runtime environment we are in. You can customize this by
// setting the ENVIRONMENT setting at compile time (see settings.js).

// Attempt to auto-detect the environment
var ENVIRONMENT_IS_WEB = typeof window == 'object';
var ENVIRONMENT_IS_WORKER = typeof importScripts == 'function';
// N.b. Electron.js environment is simultaneously a NODE-environment, but
// also a web environment.
var ENVIRONMENT_IS_NODE = typeof process == 'object' && typeof process.versions == 'object' && typeof process.versions.node == 'string';
var ENVIRONMENT_IS_SHELL = !ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_NODE && !ENVIRONMENT_IS_WORKER;

// `/` should be present at the end if `scriptDirectory` is not empty
var scriptDirectory = '';
function locateFile(path) {
  if (Module['locateFile']) {
    return Module['locateFile'](path, scriptDirectory);
  }
  return scriptDirectory + path;
}

// Hooks that are implemented differently in different runtime environments.
var read_,
    readAsync,
    readBinary,
    setWindowTitle;

// Normally we don't log exceptions but instead let them bubble out the top
// level where the embedding environment (e.g. the browser) can handle
// them.
// However under v8 and node we sometimes exit the process direcly in which case
// its up to use us to log the exception before exiting.
// If we fix https://github.com/emscripten-core/emscripten/issues/15080
// this may no longer be needed under node.
function logExceptionOnExit(e) {
  if (e instanceof ExitStatus) return;
  let toLog = e;
  err('exiting due to exception: ' + toLog);
}

var fs;
var nodePath;
var requireNodeFS;

if (ENVIRONMENT_IS_NODE) {
  if (ENVIRONMENT_IS_WORKER) {
    scriptDirectory = require('path').dirname(scriptDirectory) + '/';
  } else {
    scriptDirectory = __dirname + '/';
  }

// include: node_shell_read.js


requireNodeFS = () => {
  // Use nodePath as the indicator for these not being initialized,
  // since in some environments a global fs may have already been
  // created.
  if (!nodePath) {
    fs = require('fs');
    nodePath = require('path');
  }
};

read_ = function shell_read(filename, binary) {
  requireNodeFS();
  filename = nodePath['normalize'](filename);
  return fs.readFileSync(filename, binary ? undefined : 'utf8');
};

readBinary = (filename) => {
  var ret = read_(filename, true);
  if (!ret.buffer) {
    ret = new Uint8Array(ret);
  }
  return ret;
};

readAsync = (filename, onload, onerror) => {
  requireNodeFS();
  filename = nodePath['normalize'](filename);
  fs.readFile(filename, function(err, data) {
    if (err) onerror(err);
    else onload(data.buffer);
  });
};

// end include: node_shell_read.js
  if (process['argv'].length > 1) {
    thisProgram = process['argv'][1].replace(/\\/g, '/');
  }

  arguments_ = process['argv'].slice(2);

  // MODULARIZE will export the module in the proper place outside, we don't need to export here

  process['on']('uncaughtException', function(ex) {
    // suppress ExitStatus exceptions from showing an error
    if (!(ex instanceof ExitStatus)) {
      throw ex;
    }
  });

  // Without this older versions of node (< v15) will log unhandled rejections
  // but return 0, which is not normally the desired behaviour.  This is
  // not be needed with node v15 and about because it is now the default
  // behaviour:
  // See https://nodejs.org/api/cli.html#cli_unhandled_rejections_mode
  process['on']('unhandledRejection', function(reason) { throw reason; });

  quit_ = (status, toThrow) => {
    if (keepRuntimeAlive()) {
      process['exitCode'] = status;
      throw toThrow;
    }
    logExceptionOnExit(toThrow);
    process['exit'](status);
  };

  Module['inspect'] = function () { return '[Emscripten Module object]'; };

} else

// Note that this includes Node.js workers when relevant (pthreads is enabled).
// Node.js workers are detected as a combination of ENVIRONMENT_IS_WORKER and
// ENVIRONMENT_IS_NODE.
if (ENVIRONMENT_IS_WEB || ENVIRONMENT_IS_WORKER) {
  if (ENVIRONMENT_IS_WORKER) { // Check worker, not web, since window could be polyfilled
    scriptDirectory = self.location.href;
  } else if (typeof document != 'undefined' && document.currentScript) { // web
    scriptDirectory = document.currentScript.src;
  }
  // When MODULARIZE, this JS may be executed later, after document.currentScript
  // is gone, so we saved it, and we use it here instead of any other info.
  if (_scriptDir) {
    scriptDirectory = _scriptDir;
  }
  // blob urls look like blob:http://site.com/etc/etc and we cannot infer anything from them.
  // otherwise, slice off the final part of the url to find the script directory.
  // if scriptDirectory does not contain a slash, lastIndexOf will return -1,
  // and scriptDirectory will correctly be replaced with an empty string.
  // If scriptDirectory contains a query (starting with ?) or a fragment (starting with #),
  // they are removed because they could contain a slash.
  if (scriptDirectory.indexOf('blob:') !== 0) {
    scriptDirectory = scriptDirectory.substr(0, scriptDirectory.replace(/[?#].*/, "").lastIndexOf('/')+1);
  } else {
    scriptDirectory = '';
  }

  // Differentiate the Web Worker from the Node Worker case, as reading must
  // be done differently.
  {
// include: web_or_worker_shell_read.js


  read_ = (url) => {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url, false);
      xhr.send(null);
      return xhr.responseText;
  }

  if (ENVIRONMENT_IS_WORKER) {
    readBinary = (url) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, false);
        xhr.responseType = 'arraybuffer';
        xhr.send(null);
        return new Uint8Array(/** @type{!ArrayBuffer} */(xhr.response));
    };
  }

  readAsync = (url, onload, onerror) => {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'arraybuffer';
    xhr.onload = () => {
      if (xhr.status == 200 || (xhr.status == 0 && xhr.response)) { // file URLs can return 0
        onload(xhr.response);
        return;
      }
      onerror();
    };
    xhr.onerror = onerror;
    xhr.send(null);
  }

// end include: web_or_worker_shell_read.js
  }

  setWindowTitle = (title) => document.title = title;
} else
{
}

var out = Module['print'] || console.log.bind(console);
var err = Module['printErr'] || console.warn.bind(console);

// Merge back in the overrides
Object.assign(Module, moduleOverrides);
// Free the object hierarchy contained in the overrides, this lets the GC
// reclaim data used e.g. in memoryInitializerRequest, which is a large typed array.
moduleOverrides = null;

// Emit code to handle expected values on the Module object. This applies Module.x
// to the proper local x. This has two benefits: first, we only emit it if it is
// expected to arrive, and second, by using a local everywhere else that can be
// minified.

if (Module['arguments']) arguments_ = Module['arguments'];

if (Module['thisProgram']) thisProgram = Module['thisProgram'];

if (Module['quit']) quit_ = Module['quit'];

// perform assertions in shell.js after we set up out() and err(), as otherwise if an assertion fails it cannot print the message




var STACK_ALIGN = 16;
var POINTER_SIZE = 4;

function getNativeTypeSize(type) {
  switch (type) {
    case 'i1': case 'i8': return 1;
    case 'i16': return 2;
    case 'i32': return 4;
    case 'i64': return 8;
    case 'float': return 4;
    case 'double': return 8;
    default: {
      if (type[type.length - 1] === '*') {
        return POINTER_SIZE;
      } else if (type[0] === 'i') {
        const bits = Number(type.substr(1));
        assert(bits % 8 === 0, 'getNativeTypeSize invalid bits ' + bits + ', type ' + type);
        return bits / 8;
      } else {
        return 0;
      }
    }
  }
}

function warnOnce(text) {
  if (!warnOnce.shown) warnOnce.shown = {};
  if (!warnOnce.shown[text]) {
    warnOnce.shown[text] = 1;
    err(text);
  }
}

// include: runtime_functions.js


// Wraps a JS function as a wasm function with a given signature.
function convertJsFunctionToWasm(func, sig) {

  // If the type reflection proposal is available, use the new
  // "WebAssembly.Function" constructor.
  // Otherwise, construct a minimal wasm module importing the JS function and
  // re-exporting it.
  if (typeof WebAssembly.Function == "function") {
    var typeNames = {
      'i': 'i32',
      'j': 'i64',
      'f': 'f32',
      'd': 'f64'
    };
    var type = {
      parameters: [],
      results: sig[0] == 'v' ? [] : [typeNames[sig[0]]]
    };
    for (var i = 1; i < sig.length; ++i) {
      type.parameters.push(typeNames[sig[i]]);
    }
    return new WebAssembly.Function(type, func);
  }

  // The module is static, with the exception of the type section, which is
  // generated based on the signature passed in.
  var typeSection = [
    0x01, // id: section,
    0x00, // length: 0 (placeholder)
    0x01, // count: 1
    0x60, // form: func
  ];
  var sigRet = sig.slice(0, 1);
  var sigParam = sig.slice(1);
  var typeCodes = {
    'i': 0x7f, // i32
    'j': 0x7e, // i64
    'f': 0x7d, // f32
    'd': 0x7c, // f64
  };

  // Parameters, length + signatures
  typeSection.push(sigParam.length);
  for (var i = 0; i < sigParam.length; ++i) {
    typeSection.push(typeCodes[sigParam[i]]);
  }

  // Return values, length + signatures
  // With no multi-return in MVP, either 0 (void) or 1 (anything else)
  if (sigRet == 'v') {
    typeSection.push(0x00);
  } else {
    typeSection = typeSection.concat([0x01, typeCodes[sigRet]]);
  }

  // Write the overall length of the type section back into the section header
  // (excepting the 2 bytes for the section id and length)
  typeSection[1] = typeSection.length - 2;

  // Rest of the module is static
  var bytes = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, // magic ("\0asm")
    0x01, 0x00, 0x00, 0x00, // version: 1
  ].concat(typeSection, [
    0x02, 0x07, // import section
      // (import "e" "f" (func 0 (type 0)))
      0x01, 0x01, 0x65, 0x01, 0x66, 0x00, 0x00,
    0x07, 0x05, // export section
      // (export "f" (func 0 (type 0)))
      0x01, 0x01, 0x66, 0x00, 0x00,
  ]));

   // We can compile this wasm module synchronously because it is very small.
  // This accepts an import (at "e.f"), that it reroutes to an export (at "f")
  var module = new WebAssembly.Module(bytes);
  var instance = new WebAssembly.Instance(module, {
    'e': {
      'f': func
    }
  });
  var wrappedFunc = instance.exports['f'];
  return wrappedFunc;
}

var freeTableIndexes = [];

// Weak map of functions in the table to their indexes, created on first use.
var functionsInTableMap;

function getEmptyTableSlot() {
  // Reuse a free index if there is one, otherwise grow.
  if (freeTableIndexes.length) {
    return freeTableIndexes.pop();
  }
  // Grow the table
  try {
    wasmTable.grow(1);
  } catch (err) {
    if (!(err instanceof RangeError)) {
      throw err;
    }
    throw 'Unable to grow wasm table. Set ALLOW_TABLE_GROWTH.';
  }
  return wasmTable.length - 1;
}

function updateTableMap(offset, count) {
  for (var i = offset; i < offset + count; i++) {
    var item = getWasmTableEntry(i);
    // Ignore null values.
    if (item) {
      functionsInTableMap.set(item, i);
    }
  }
}

/**
 * Add a function to the table.
 * 'sig' parameter is required if the function being added is a JS function.
 * @param {string=} sig
 */
function addFunction(func, sig) {

  // Check if the function is already in the table, to ensure each function
  // gets a unique index. First, create the map if this is the first use.
  if (!functionsInTableMap) {
    functionsInTableMap = new WeakMap();
    updateTableMap(0, wasmTable.length);
  }
  if (functionsInTableMap.has(func)) {
    return functionsInTableMap.get(func);
  }

  // It's not in the table, add it now.

  var ret = getEmptyTableSlot();

  // Set the new value.
  try {
    // Attempting to call this with JS function will cause of table.set() to fail
    setWasmTableEntry(ret, func);
  } catch (err) {
    if (!(err instanceof TypeError)) {
      throw err;
    }
    var wrapped = convertJsFunctionToWasm(func, sig);
    setWasmTableEntry(ret, wrapped);
  }

  functionsInTableMap.set(func, ret);

  return ret;
}

function removeFunction(index) {
  functionsInTableMap.delete(getWasmTableEntry(index));
  freeTableIndexes.push(index);
}

// end include: runtime_functions.js
// include: runtime_debug.js


// end include: runtime_debug.js
var tempRet0 = 0;
var setTempRet0 = (value) => { tempRet0 = value; };
var getTempRet0 = () => tempRet0;



// === Preamble library stuff ===

// Documentation for the public APIs defined in this file must be updated in:
//    site/source/docs/api_reference/preamble.js.rst
// A prebuilt local version of the documentation is available at:
//    site/build/text/docs/api_reference/preamble.js.txt
// You can also build docs locally as HTML or other formats in site/
// An online HTML version (which may be of a different version of Emscripten)
//    is up at http://kripken.github.io/emscripten-site/docs/api_reference/preamble.js.html

var wasmBinary;
if (Module['wasmBinary']) wasmBinary = Module['wasmBinary'];
var noExitRuntime = Module['noExitRuntime'] || true;

if (typeof WebAssembly != 'object') {
  abort('no native wasm support detected');
}

// include: runtime_safe_heap.js


// In MINIMAL_RUNTIME, setValue() and getValue() are only available when building with safe heap enabled, for heap safety checking.
// In traditional runtime, setValue() and getValue() are always available (although their use is highly discouraged due to perf penalties)

/** @param {number} ptr
    @param {number} value
    @param {string} type
    @param {number|boolean=} noSafe */
function setValue(ptr, value, type = 'i8', noSafe) {
  if (type.charAt(type.length-1) === '*') type = 'i32';
    switch (type) {
      case 'i1': HEAP8[((ptr)>>0)] = value; break;
      case 'i8': HEAP8[((ptr)>>0)] = value; break;
      case 'i16': HEAP16[((ptr)>>1)] = value; break;
      case 'i32': HEAP32[((ptr)>>2)] = value; break;
      case 'i64': (tempI64 = [value>>>0,(tempDouble=value,(+(Math.abs(tempDouble))) >= 1.0 ? (tempDouble > 0.0 ? ((Math.min((+(Math.floor((tempDouble)/4294967296.0))), 4294967295.0))|0)>>>0 : (~~((+(Math.ceil((tempDouble - +(((~~(tempDouble)))>>>0))/4294967296.0)))))>>>0) : 0)],HEAP32[((ptr)>>2)] = tempI64[0],HEAP32[(((ptr)+(4))>>2)] = tempI64[1]); break;
      case 'float': HEAPF32[((ptr)>>2)] = value; break;
      case 'double': HEAPF64[((ptr)>>3)] = value; break;
      default: abort('invalid type for setValue: ' + type);
    }
}

/** @param {number} ptr
    @param {string} type
    @param {number|boolean=} noSafe */
function getValue(ptr, type = 'i8', noSafe) {
  if (type.charAt(type.length-1) === '*') type = 'i32';
    switch (type) {
      case 'i1': return HEAP8[((ptr)>>0)];
      case 'i8': return HEAP8[((ptr)>>0)];
      case 'i16': return HEAP16[((ptr)>>1)];
      case 'i32': return HEAP32[((ptr)>>2)];
      case 'i64': return HEAP32[((ptr)>>2)];
      case 'float': return HEAPF32[((ptr)>>2)];
      case 'double': return Number(HEAPF64[((ptr)>>3)]);
      default: abort('invalid type for getValue: ' + type);
    }
  return null;
}

// end include: runtime_safe_heap.js
// Wasm globals

var wasmMemory;

//========================================
// Runtime essentials
//========================================

// whether we are quitting the application. no code should run after this.
// set in exit() and abort()
var ABORT = false;

// set by exit() and abort().  Passed to 'onExit' handler.
// NOTE: This is also used as the process return code code in shell environments
// but only when noExitRuntime is false.
var EXITSTATUS;

/** @type {function(*, string=)} */
function assert(condition, text) {
  if (!condition) {
    // This build was created without ASSERTIONS defined.  `assert()` should not
    // ever be called in this configuration but in case there are callers in
    // the wild leave this simple abort() implemenation here for now.
    abort(text);
  }
}

// Returns the C function with a specified identifier (for C++, you need to do manual name mangling)
function getCFunc(ident) {
  var func = Module['_' + ident]; // closure exported function
  return func;
}

// C calling interface.
/** @param {string|null=} returnType
    @param {Array=} argTypes
    @param {Arguments|Array=} args
    @param {Object=} opts */
function ccall(ident, returnType, argTypes, args, opts) {
  // For fast lookup of conversion functions
  var toC = {
    'string': function(str) {
      var ret = 0;
      if (str !== null && str !== undefined && str !== 0) { // null string
        // at most 4 bytes per UTF-8 code point, +1 for the trailing '\0'
        var len = (str.length << 2) + 1;
        ret = stackAlloc(len);
        stringToUTF8(str, ret, len);
      }
      return ret;
    },
    'array': function(arr) {
      var ret = stackAlloc(arr.length);
      writeArrayToMemory(arr, ret);
      return ret;
    }
  };

  function convertReturnValue(ret) {
    if (returnType === 'string') return UTF8ToString(ret);
    if (returnType === 'boolean') return Boolean(ret);
    return ret;
  }

  var func = getCFunc(ident);
  var cArgs = [];
  var stack = 0;
  if (args) {
    for (var i = 0; i < args.length; i++) {
      var converter = toC[argTypes[i]];
      if (converter) {
        if (stack === 0) stack = stackSave();
        cArgs[i] = converter(args[i]);
      } else {
        cArgs[i] = args[i];
      }
    }
  }
  var ret = func.apply(null, cArgs);
  function onDone(ret) {
    if (stack !== 0) stackRestore(stack);
    return convertReturnValue(ret);
  }

  ret = onDone(ret);
  return ret;
}

/** @param {string=} returnType
    @param {Array=} argTypes
    @param {Object=} opts */
function cwrap(ident, returnType, argTypes, opts) {
  argTypes = argTypes || [];
  // When the function takes numbers and returns a number, we can just return
  // the original function
  var numericArgs = argTypes.every(function(type){ return type === 'number'});
  var numericRet = returnType !== 'string';
  if (numericRet && numericArgs && !opts) {
    return getCFunc(ident);
  }
  return function() {
    return ccall(ident, returnType, argTypes, arguments, opts);
  }
}

// include: runtime_legacy.js


var ALLOC_NORMAL = 0; // Tries to use _malloc()
var ALLOC_STACK = 1; // Lives for the duration of the current function call

/**
 * allocate(): This function is no longer used by emscripten but is kept around to avoid
 *             breaking external users.
 *             You should normally not use allocate(), and instead allocate
 *             memory using _malloc()/stackAlloc(), initialize it with
 *             setValue(), and so forth.
 * @param {(Uint8Array|Array<number>)} slab: An array of data.
 * @param {number=} allocator : How to allocate memory, see ALLOC_*
 */
function allocate(slab, allocator) {
  var ret;

  if (allocator == ALLOC_STACK) {
    ret = stackAlloc(slab.length);
  } else {
    ret = _malloc(slab.length);
  }

  if (!slab.subarray && !slab.slice) {
    slab = new Uint8Array(slab);
  }
  HEAPU8.set(slab, ret);
  return ret;
}

// end include: runtime_legacy.js
// include: runtime_strings.js


// runtime_strings.js: Strings related runtime functions that are part of both MINIMAL_RUNTIME and regular runtime.

var UTF8Decoder = typeof TextDecoder != 'undefined' ? new TextDecoder('utf8') : undefined;

// Given a pointer 'ptr' to a null-terminated UTF8-encoded string in the given array that contains uint8 values, returns
// a copy of that string as a Javascript String object.
/**
 * heapOrArray is either a regular array, or a JavaScript typed array view.
 * @param {number} idx
 * @param {number=} maxBytesToRead
 * @return {string}
 */
function UTF8ArrayToString(heapOrArray, idx, maxBytesToRead) {
  var endIdx = idx + maxBytesToRead;
  var endPtr = idx;
  // TextDecoder needs to know the byte length in advance, it doesn't stop on null terminator by itself.
  // Also, use the length info to avoid running tiny strings through TextDecoder, since .subarray() allocates garbage.
  // (As a tiny code save trick, compare endPtr against endIdx using a negation, so that undefined means Infinity)
  while (heapOrArray[endPtr] && !(endPtr >= endIdx)) ++endPtr;

  if (endPtr - idx > 16 && heapOrArray.buffer && UTF8Decoder) {
    return UTF8Decoder.decode(heapOrArray.subarray(idx, endPtr));
  } else {
    var str = '';
    // If building with TextDecoder, we have already computed the string length above, so test loop end condition against that
    while (idx < endPtr) {
      // For UTF8 byte structure, see:
      // http://en.wikipedia.org/wiki/UTF-8#Description
      // https://www.ietf.org/rfc/rfc2279.txt
      // https://tools.ietf.org/html/rfc3629
      var u0 = heapOrArray[idx++];
      if (!(u0 & 0x80)) { str += String.fromCharCode(u0); continue; }
      var u1 = heapOrArray[idx++] & 63;
      if ((u0 & 0xE0) == 0xC0) { str += String.fromCharCode(((u0 & 31) << 6) | u1); continue; }
      var u2 = heapOrArray[idx++] & 63;
      if ((u0 & 0xF0) == 0xE0) {
        u0 = ((u0 & 15) << 12) | (u1 << 6) | u2;
      } else {
        u0 = ((u0 & 7) << 18) | (u1 << 12) | (u2 << 6) | (heapOrArray[idx++] & 63);
      }

      if (u0 < 0x10000) {
        str += String.fromCharCode(u0);
      } else {
        var ch = u0 - 0x10000;
        str += String.fromCharCode(0xD800 | (ch >> 10), 0xDC00 | (ch & 0x3FF));
      }
    }
  }
  return str;
}

// Given a pointer 'ptr' to a null-terminated UTF8-encoded string in the emscripten HEAP, returns a
// copy of that string as a Javascript String object.
// maxBytesToRead: an optional length that specifies the maximum number of bytes to read. You can omit
//                 this parameter to scan the string until the first \0 byte. If maxBytesToRead is
//                 passed, and the string at [ptr, ptr+maxBytesToReadr[ contains a null byte in the
//                 middle, then the string will cut short at that byte index (i.e. maxBytesToRead will
//                 not produce a string of exact length [ptr, ptr+maxBytesToRead[)
//                 N.B. mixing frequent uses of UTF8ToString() with and without maxBytesToRead may
//                 throw JS JIT optimizations off, so it is worth to consider consistently using one
//                 style or the other.
/**
 * @param {number} ptr
 * @param {number=} maxBytesToRead
 * @return {string}
 */
function UTF8ToString(ptr, maxBytesToRead) {
  ;
  return ptr ? UTF8ArrayToString(HEAPU8, ptr, maxBytesToRead) : '';
}

// Copies the given Javascript String object 'str' to the given byte array at address 'outIdx',
// encoded in UTF8 form and null-terminated. The copy will require at most str.length*4+1 bytes of space in the HEAP.
// Use the function lengthBytesUTF8 to compute the exact number of bytes (excluding null terminator) that this function will write.
// Parameters:
//   str: the Javascript string to copy.
//   heap: the array to copy to. Each index in this array is assumed to be one 8-byte element.
//   outIdx: The starting offset in the array to begin the copying.
//   maxBytesToWrite: The maximum number of bytes this function can write to the array.
//                    This count should include the null terminator,
//                    i.e. if maxBytesToWrite=1, only the null terminator will be written and nothing else.
//                    maxBytesToWrite=0 does not write any bytes to the output, not even the null terminator.
// Returns the number of bytes written, EXCLUDING the null terminator.

function stringToUTF8Array(str, heap, outIdx, maxBytesToWrite) {
  if (!(maxBytesToWrite > 0)) // Parameter maxBytesToWrite is not optional. Negative values, 0, null, undefined and false each don't write out any bytes.
    return 0;

  var startIdx = outIdx;
  var endIdx = outIdx + maxBytesToWrite - 1; // -1 for string null terminator.
  for (var i = 0; i < str.length; ++i) {
    // Gotcha: charCodeAt returns a 16-bit word that is a UTF-16 encoded code unit, not a Unicode code point of the character! So decode UTF16->UTF32->UTF8.
    // See http://unicode.org/faq/utf_bom.html#utf16-3
    // For UTF8 byte structure, see http://en.wikipedia.org/wiki/UTF-8#Description and https://www.ietf.org/rfc/rfc2279.txt and https://tools.ietf.org/html/rfc3629
    var u = str.charCodeAt(i); // possibly a lead surrogate
    if (u >= 0xD800 && u <= 0xDFFF) {
      var u1 = str.charCodeAt(++i);
      u = 0x10000 + ((u & 0x3FF) << 10) | (u1 & 0x3FF);
    }
    if (u <= 0x7F) {
      if (outIdx >= endIdx) break;
      heap[outIdx++] = u;
    } else if (u <= 0x7FF) {
      if (outIdx + 1 >= endIdx) break;
      heap[outIdx++] = 0xC0 | (u >> 6);
      heap[outIdx++] = 0x80 | (u & 63);
    } else if (u <= 0xFFFF) {
      if (outIdx + 2 >= endIdx) break;
      heap[outIdx++] = 0xE0 | (u >> 12);
      heap[outIdx++] = 0x80 | ((u >> 6) & 63);
      heap[outIdx++] = 0x80 | (u & 63);
    } else {
      if (outIdx + 3 >= endIdx) break;
      heap[outIdx++] = 0xF0 | (u >> 18);
      heap[outIdx++] = 0x80 | ((u >> 12) & 63);
      heap[outIdx++] = 0x80 | ((u >> 6) & 63);
      heap[outIdx++] = 0x80 | (u & 63);
    }
  }
  // Null-terminate the pointer to the buffer.
  heap[outIdx] = 0;
  return outIdx - startIdx;
}

// Copies the given Javascript String object 'str' to the emscripten HEAP at address 'outPtr',
// null-terminated and encoded in UTF8 form. The copy will require at most str.length*4+1 bytes of space in the HEAP.
// Use the function lengthBytesUTF8 to compute the exact number of bytes (excluding null terminator) that this function will write.
// Returns the number of bytes written, EXCLUDING the null terminator.

function stringToUTF8(str, outPtr, maxBytesToWrite) {
  return stringToUTF8Array(str, HEAPU8,outPtr, maxBytesToWrite);
}

// Returns the number of bytes the given Javascript string takes if encoded as a UTF8 byte array, EXCLUDING the null terminator byte.
function lengthBytesUTF8(str) {
  var len = 0;
  for (var i = 0; i < str.length; ++i) {
    // Gotcha: charCodeAt returns a 16-bit word that is a UTF-16 encoded code unit, not a Unicode code point of the character! So decode UTF16->UTF32->UTF8.
    // See http://unicode.org/faq/utf_bom.html#utf16-3
    var u = str.charCodeAt(i); // possibly a lead surrogate
    if (u >= 0xD800 && u <= 0xDFFF) u = 0x10000 + ((u & 0x3FF) << 10) | (str.charCodeAt(++i) & 0x3FF);
    if (u <= 0x7F) ++len;
    else if (u <= 0x7FF) len += 2;
    else if (u <= 0xFFFF) len += 3;
    else len += 4;
  }
  return len;
}

// end include: runtime_strings.js
// include: runtime_strings_extra.js


// runtime_strings_extra.js: Strings related runtime functions that are available only in regular runtime.

// Given a pointer 'ptr' to a null-terminated ASCII-encoded string in the emscripten HEAP, returns
// a copy of that string as a Javascript String object.

function AsciiToString(ptr) {
  var str = '';
  while (1) {
    var ch = HEAPU8[((ptr++)>>0)];
    if (!ch) return str;
    str += String.fromCharCode(ch);
  }
}

// Copies the given Javascript String object 'str' to the emscripten HEAP at address 'outPtr',
// null-terminated and encoded in ASCII form. The copy will require at most str.length+1 bytes of space in the HEAP.

function stringToAscii(str, outPtr) {
  return writeAsciiToMemory(str, outPtr, false);
}

// Given a pointer 'ptr' to a null-terminated UTF16LE-encoded string in the emscripten HEAP, returns
// a copy of that string as a Javascript String object.

var UTF16Decoder = typeof TextDecoder != 'undefined' ? new TextDecoder('utf-16le') : undefined;

function UTF16ToString(ptr, maxBytesToRead) {
  var endPtr = ptr;
  // TextDecoder needs to know the byte length in advance, it doesn't stop on null terminator by itself.
  // Also, use the length info to avoid running tiny strings through TextDecoder, since .subarray() allocates garbage.
  var idx = endPtr >> 1;
  var maxIdx = idx + maxBytesToRead / 2;
  // If maxBytesToRead is not passed explicitly, it will be undefined, and this
  // will always evaluate to true. This saves on code size.
  while (!(idx >= maxIdx) && HEAPU16[idx]) ++idx;
  endPtr = idx << 1;

  if (endPtr - ptr > 32 && UTF16Decoder) {
    return UTF16Decoder.decode(HEAPU8.subarray(ptr, endPtr));
  } else {
    var str = '';

    // If maxBytesToRead is not passed explicitly, it will be undefined, and the for-loop's condition
    // will always evaluate to true. The loop is then terminated on the first null char.
    for (var i = 0; !(i >= maxBytesToRead / 2); ++i) {
      var codeUnit = HEAP16[(((ptr)+(i*2))>>1)];
      if (codeUnit == 0) break;
      // fromCharCode constructs a character from a UTF-16 code unit, so we can pass the UTF16 string right through.
      str += String.fromCharCode(codeUnit);
    }

    return str;
  }
}

// Copies the given Javascript String object 'str' to the emscripten HEAP at address 'outPtr',
// null-terminated and encoded in UTF16 form. The copy will require at most str.length*4+2 bytes of space in the HEAP.
// Use the function lengthBytesUTF16() to compute the exact number of bytes (excluding null terminator) that this function will write.
// Parameters:
//   str: the Javascript string to copy.
//   outPtr: Byte address in Emscripten HEAP where to write the string to.
//   maxBytesToWrite: The maximum number of bytes this function can write to the array. This count should include the null
//                    terminator, i.e. if maxBytesToWrite=2, only the null terminator will be written and nothing else.
//                    maxBytesToWrite<2 does not write any bytes to the output, not even the null terminator.
// Returns the number of bytes written, EXCLUDING the null terminator.

function stringToUTF16(str, outPtr, maxBytesToWrite) {
  // Backwards compatibility: if max bytes is not specified, assume unsafe unbounded write is allowed.
  if (maxBytesToWrite === undefined) {
    maxBytesToWrite = 0x7FFFFFFF;
  }
  if (maxBytesToWrite < 2) return 0;
  maxBytesToWrite -= 2; // Null terminator.
  var startPtr = outPtr;
  var numCharsToWrite = (maxBytesToWrite < str.length*2) ? (maxBytesToWrite / 2) : str.length;
  for (var i = 0; i < numCharsToWrite; ++i) {
    // charCodeAt returns a UTF-16 encoded code unit, so it can be directly written to the HEAP.
    var codeUnit = str.charCodeAt(i); // possibly a lead surrogate
    HEAP16[((outPtr)>>1)] = codeUnit;
    outPtr += 2;
  }
  // Null-terminate the pointer to the HEAP.
  HEAP16[((outPtr)>>1)] = 0;
  return outPtr - startPtr;
}

// Returns the number of bytes the given Javascript string takes if encoded as a UTF16 byte array, EXCLUDING the null terminator byte.

function lengthBytesUTF16(str) {
  return str.length*2;
}

function UTF32ToString(ptr, maxBytesToRead) {
  var i = 0;

  var str = '';
  // If maxBytesToRead is not passed explicitly, it will be undefined, and this
  // will always evaluate to true. This saves on code size.
  while (!(i >= maxBytesToRead / 4)) {
    var utf32 = HEAP32[(((ptr)+(i*4))>>2)];
    if (utf32 == 0) break;
    ++i;
    // Gotcha: fromCharCode constructs a character from a UTF-16 encoded code (pair), not from a Unicode code point! So encode the code point to UTF-16 for constructing.
    // See http://unicode.org/faq/utf_bom.html#utf16-3
    if (utf32 >= 0x10000) {
      var ch = utf32 - 0x10000;
      str += String.fromCharCode(0xD800 | (ch >> 10), 0xDC00 | (ch & 0x3FF));
    } else {
      str += String.fromCharCode(utf32);
    }
  }
  return str;
}

// Copies the given Javascript String object 'str' to the emscripten HEAP at address 'outPtr',
// null-terminated and encoded in UTF32 form. The copy will require at most str.length*4+4 bytes of space in the HEAP.
// Use the function lengthBytesUTF32() to compute the exact number of bytes (excluding null terminator) that this function will write.
// Parameters:
//   str: the Javascript string to copy.
//   outPtr: Byte address in Emscripten HEAP where to write the string to.
//   maxBytesToWrite: The maximum number of bytes this function can write to the array. This count should include the null
//                    terminator, i.e. if maxBytesToWrite=4, only the null terminator will be written and nothing else.
//                    maxBytesToWrite<4 does not write any bytes to the output, not even the null terminator.
// Returns the number of bytes written, EXCLUDING the null terminator.

function stringToUTF32(str, outPtr, maxBytesToWrite) {
  // Backwards compatibility: if max bytes is not specified, assume unsafe unbounded write is allowed.
  if (maxBytesToWrite === undefined) {
    maxBytesToWrite = 0x7FFFFFFF;
  }
  if (maxBytesToWrite < 4) return 0;
  var startPtr = outPtr;
  var endPtr = startPtr + maxBytesToWrite - 4;
  for (var i = 0; i < str.length; ++i) {
    // Gotcha: charCodeAt returns a 16-bit word that is a UTF-16 encoded code unit, not a Unicode code point of the character! We must decode the string to UTF-32 to the heap.
    // See http://unicode.org/faq/utf_bom.html#utf16-3
    var codeUnit = str.charCodeAt(i); // possibly a lead surrogate
    if (codeUnit >= 0xD800 && codeUnit <= 0xDFFF) {
      var trailSurrogate = str.charCodeAt(++i);
      codeUnit = 0x10000 + ((codeUnit & 0x3FF) << 10) | (trailSurrogate & 0x3FF);
    }
    HEAP32[((outPtr)>>2)] = codeUnit;
    outPtr += 4;
    if (outPtr + 4 > endPtr) break;
  }
  // Null-terminate the pointer to the HEAP.
  HEAP32[((outPtr)>>2)] = 0;
  return outPtr - startPtr;
}

// Returns the number of bytes the given Javascript string takes if encoded as a UTF16 byte array, EXCLUDING the null terminator byte.

function lengthBytesUTF32(str) {
  var len = 0;
  for (var i = 0; i < str.length; ++i) {
    // Gotcha: charCodeAt returns a 16-bit word that is a UTF-16 encoded code unit, not a Unicode code point of the character! We must decode the string to UTF-32 to the heap.
    // See http://unicode.org/faq/utf_bom.html#utf16-3
    var codeUnit = str.charCodeAt(i);
    if (codeUnit >= 0xD800 && codeUnit <= 0xDFFF) ++i; // possibly a lead surrogate, so skip over the tail surrogate.
    len += 4;
  }

  return len;
}

// Allocate heap space for a JS string, and write it there.
// It is the responsibility of the caller to free() that memory.
function allocateUTF8(str) {
  var size = lengthBytesUTF8(str) + 1;
  var ret = _malloc(size);
  if (ret) stringToUTF8Array(str, HEAP8, ret, size);
  return ret;
}

// Allocate stack space for a JS string, and write it there.
function allocateUTF8OnStack(str) {
  var size = lengthBytesUTF8(str) + 1;
  var ret = stackAlloc(size);
  stringToUTF8Array(str, HEAP8, ret, size);
  return ret;
}

// Deprecated: This function should not be called because it is unsafe and does not provide
// a maximum length limit of how many bytes it is allowed to write. Prefer calling the
// function stringToUTF8Array() instead, which takes in a maximum length that can be used
// to be secure from out of bounds writes.
/** @deprecated
    @param {boolean=} dontAddNull */
function writeStringToMemory(string, buffer, dontAddNull) {
  warnOnce('writeStringToMemory is deprecated and should not be called! Use stringToUTF8() instead!');

  var /** @type {number} */ lastChar, /** @type {number} */ end;
  if (dontAddNull) {
    // stringToUTF8Array always appends null. If we don't want to do that, remember the
    // character that existed at the location where the null will be placed, and restore
    // that after the write (below).
    end = buffer + lengthBytesUTF8(string);
    lastChar = HEAP8[end];
  }
  stringToUTF8(string, buffer, Infinity);
  if (dontAddNull) HEAP8[end] = lastChar; // Restore the value under the null character.
}

function writeArrayToMemory(array, buffer) {
  HEAP8.set(array, buffer);
}

/** @param {boolean=} dontAddNull */
function writeAsciiToMemory(str, buffer, dontAddNull) {
  for (var i = 0; i < str.length; ++i) {
    HEAP8[((buffer++)>>0)] = str.charCodeAt(i);
  }
  // Null-terminate the pointer to the HEAP.
  if (!dontAddNull) HEAP8[((buffer)>>0)] = 0;
}

// end include: runtime_strings_extra.js
// Memory management

var HEAP,
/** @type {!ArrayBuffer} */
  buffer,
/** @type {!Int8Array} */
  HEAP8,
/** @type {!Uint8Array} */
  HEAPU8,
/** @type {!Int16Array} */
  HEAP16,
/** @type {!Uint16Array} */
  HEAPU16,
/** @type {!Int32Array} */
  HEAP32,
/** @type {!Uint32Array} */
  HEAPU32,
/** @type {!Float32Array} */
  HEAPF32,
/** @type {!Float64Array} */
  HEAPF64;

function updateGlobalBufferAndViews(buf) {
  buffer = buf;
  Module['HEAP8'] = HEAP8 = new Int8Array(buf);
  Module['HEAP16'] = HEAP16 = new Int16Array(buf);
  Module['HEAP32'] = HEAP32 = new Int32Array(buf);
  Module['HEAPU8'] = HEAPU8 = new Uint8Array(buf);
  Module['HEAPU16'] = HEAPU16 = new Uint16Array(buf);
  Module['HEAPU32'] = HEAPU32 = new Uint32Array(buf);
  Module['HEAPF32'] = HEAPF32 = new Float32Array(buf);
  Module['HEAPF64'] = HEAPF64 = new Float64Array(buf);
}

var TOTAL_STACK = 5242880;

var INITIAL_MEMORY = Module['INITIAL_MEMORY'] || 33554432;

// include: runtime_init_table.js
// In regular non-RELOCATABLE mode the table is exported
// from the wasm module and this will be assigned once
// the exports are available.
var wasmTable;

// end include: runtime_init_table.js
// include: runtime_stack_check.js


// end include: runtime_stack_check.js
// include: runtime_assertions.js


// end include: runtime_assertions.js
var __ATPRERUN__  = []; // functions called before the runtime is initialized
var __ATINIT__    = []; // functions called during startup
var __ATEXIT__    = []; // functions called during shutdown
var __ATPOSTRUN__ = []; // functions called after the main() is called

var runtimeInitialized = false;

function keepRuntimeAlive() {
  return noExitRuntime;
}

function preRun() {

  if (Module['preRun']) {
    if (typeof Module['preRun'] == 'function') Module['preRun'] = [Module['preRun']];
    while (Module['preRun'].length) {
      addOnPreRun(Module['preRun'].shift());
    }
  }

  callRuntimeCallbacks(__ATPRERUN__);
}

function initRuntime() {
  runtimeInitialized = true;

  
  callRuntimeCallbacks(__ATINIT__);
}

function postRun() {

  if (Module['postRun']) {
    if (typeof Module['postRun'] == 'function') Module['postRun'] = [Module['postRun']];
    while (Module['postRun'].length) {
      addOnPostRun(Module['postRun'].shift());
    }
  }

  callRuntimeCallbacks(__ATPOSTRUN__);
}

function addOnPreRun(cb) {
  __ATPRERUN__.unshift(cb);
}

function addOnInit(cb) {
  __ATINIT__.unshift(cb);
}

function addOnExit(cb) {
}

function addOnPostRun(cb) {
  __ATPOSTRUN__.unshift(cb);
}

// include: runtime_math.js


// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/imul

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/fround

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/clz32

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/trunc

// end include: runtime_math.js
// A counter of dependencies for calling run(). If we need to
// do asynchronous work before running, increment this and
// decrement it. Incrementing must happen in a place like
// Module.preRun (used by emcc to add file preloading).
// Note that you can add dependencies in preRun, even though
// it happens right before run - run will be postponed until
// the dependencies are met.
var runDependencies = 0;
var runDependencyWatcher = null;
var dependenciesFulfilled = null; // overridden to take different actions when all run dependencies are fulfilled

function getUniqueRunDependency(id) {
  return id;
}

function addRunDependency(id) {
  runDependencies++;

  if (Module['monitorRunDependencies']) {
    Module['monitorRunDependencies'](runDependencies);
  }

}

function removeRunDependency(id) {
  runDependencies--;

  if (Module['monitorRunDependencies']) {
    Module['monitorRunDependencies'](runDependencies);
  }

  if (runDependencies == 0) {
    if (runDependencyWatcher !== null) {
      clearInterval(runDependencyWatcher);
      runDependencyWatcher = null;
    }
    if (dependenciesFulfilled) {
      var callback = dependenciesFulfilled;
      dependenciesFulfilled = null;
      callback(); // can add another dependenciesFulfilled
    }
  }
}

Module["preloadedImages"] = {}; // maps url to image data
Module["preloadedAudios"] = {}; // maps url to audio data

/** @param {string|number=} what */
function abort(what) {
  {
    if (Module['onAbort']) {
      Module['onAbort'](what);
    }
  }

  what = 'Aborted(' + what + ')';
  // TODO(sbc): Should we remove printing and leave it up to whoever
  // catches the exception?
  err(what);

  ABORT = true;
  EXITSTATUS = 1;

  what += '. Build with -s ASSERTIONS=1 for more info.';

  // Use a wasm runtime error, because a JS error might be seen as a foreign
  // exception, which means we'd run destructors on it. We need the error to
  // simply make the program stop.

  // Suppress closure compiler warning here. Closure compiler's builtin extern
  // defintion for WebAssembly.RuntimeError claims it takes no arguments even
  // though it can.
  // TODO(https://github.com/google/closure-compiler/pull/3913): Remove if/when upstream closure gets fixed.

  /** @suppress {checkTypes} */
  var e = new WebAssembly.RuntimeError(what);

  readyPromiseReject(e);
  // Throw the error whether or not MODULARIZE is set because abort is used
  // in code paths apart from instantiation where an exception is expected
  // to be thrown when abort is called.
  throw e;
}

// {{MEM_INITIALIZER}}

// include: memoryprofiler.js


// end include: memoryprofiler.js
// include: URIUtils.js


// Prefix of data URIs emitted by SINGLE_FILE and related options.
var dataURIPrefix = 'data:application/octet-stream;base64,';

// Indicates whether filename is a base64 data URI.
function isDataURI(filename) {
  // Prefix of data URIs emitted by SINGLE_FILE and related options.
  return filename.startsWith(dataURIPrefix);
}

// Indicates whether filename is delivered via file protocol (as opposed to http/https)
function isFileURI(filename) {
  return filename.startsWith('file://');
}

// end include: URIUtils.js
var wasmBinaryFile;
  wasmBinaryFile = 'soundswallower.wasm';
  if (!isDataURI(wasmBinaryFile)) {
    wasmBinaryFile = locateFile(wasmBinaryFile);
  }

function getBinary(file) {
  try {
    if (file == wasmBinaryFile && wasmBinary) {
      return new Uint8Array(wasmBinary);
    }
    if (readBinary) {
      return readBinary(file);
    } else {
      throw "both async and sync fetching of the wasm failed";
    }
  }
  catch (err) {
    abort(err);
  }
}

function getBinaryPromise() {
  // If we don't have the binary yet, try to to load it asynchronously.
  // Fetch has some additional restrictions over XHR, like it can't be used on a file:// url.
  // See https://github.com/github/fetch/pull/92#issuecomment-140665932
  // Cordova or Electron apps are typically loaded from a file:// url.
  // So use fetch if it is available and the url is not a file, otherwise fall back to XHR.
  if (!wasmBinary && (ENVIRONMENT_IS_WEB || ENVIRONMENT_IS_WORKER)) {
    if (typeof fetch == 'function'
      && !isFileURI(wasmBinaryFile)
    ) {
      return fetch(wasmBinaryFile, { credentials: 'same-origin' }).then(function(response) {
        if (!response['ok']) {
          throw "failed to load wasm binary file at '" + wasmBinaryFile + "'";
        }
        return response['arrayBuffer']();
      }).catch(function () {
          return getBinary(wasmBinaryFile);
      });
    }
    else {
      if (readAsync) {
        // fetch is not available or url is file => try XHR (readAsync uses XHR internally)
        return new Promise(function(resolve, reject) {
          readAsync(wasmBinaryFile, function(response) { resolve(new Uint8Array(/** @type{!ArrayBuffer} */(response))) }, reject)
        });
      }
    }
  }

  // Otherwise, getBinary should be able to get it synchronously
  return Promise.resolve().then(function() { return getBinary(wasmBinaryFile); });
}

// Create the wasm instance.
// Receives the wasm imports, returns the exports.
function createWasm() {
  // prepare imports
  var info = {
    'env': asmLibraryArg,
    'wasi_snapshot_preview1': asmLibraryArg,
  };
  // Load the wasm module and create an instance of using native support in the JS engine.
  // handle a generated wasm instance, receiving its exports and
  // performing other necessary setup
  /** @param {WebAssembly.Module=} module*/
  function receiveInstance(instance, module) {
    var exports = instance.exports;

    Module['asm'] = exports;

    wasmMemory = Module['asm']['memory'];
    updateGlobalBufferAndViews(wasmMemory.buffer);

    wasmTable = Module['asm']['__indirect_function_table'];

    addOnInit(Module['asm']['__wasm_call_ctors']);

    removeRunDependency('wasm-instantiate');

  }
  // we can't run yet (except in a pthread, where we have a custom sync instantiator)
  addRunDependency('wasm-instantiate');

  // Prefer streaming instantiation if available.
  function receiveInstantiationResult(result) {
    // 'result' is a ResultObject object which has both the module and instance.
    // receiveInstance() will swap in the exports (to Module.asm) so they can be called
    // TODO: Due to Closure regression https://github.com/google/closure-compiler/issues/3193, the above line no longer optimizes out down to the following line.
    // When the regression is fixed, can restore the above USE_PTHREADS-enabled path.
    receiveInstance(result['instance']);
  }

  function instantiateArrayBuffer(receiver) {
    return getBinaryPromise().then(function(binary) {
      return WebAssembly.instantiate(binary, info);
    }).then(function (instance) {
      return instance;
    }).then(receiver, function(reason) {
      err('failed to asynchronously prepare wasm: ' + reason);

      abort(reason);
    });
  }

  function instantiateAsync() {
    if (!wasmBinary &&
        typeof WebAssembly.instantiateStreaming == 'function' &&
        !isDataURI(wasmBinaryFile) &&
        // Don't use streaming for file:// delivered objects in a webview, fetch them synchronously.
        !isFileURI(wasmBinaryFile) &&
        typeof fetch == 'function') {
      return fetch(wasmBinaryFile, { credentials: 'same-origin' }).then(function(response) {
        // Suppress closure warning here since the upstream definition for
        // instantiateStreaming only allows Promise<Repsponse> rather than
        // an actual Response.
        // TODO(https://github.com/google/closure-compiler/pull/3913): Remove if/when upstream closure is fixed.
        /** @suppress {checkTypes} */
        var result = WebAssembly.instantiateStreaming(response, info);

        return result.then(
          receiveInstantiationResult,
          function(reason) {
            // We expect the most common failure cause to be a bad MIME type for the binary,
            // in which case falling back to ArrayBuffer instantiation should work.
            err('wasm streaming compile failed: ' + reason);
            err('falling back to ArrayBuffer instantiation');
            return instantiateArrayBuffer(receiveInstantiationResult);
          });
      });
    } else {
      return instantiateArrayBuffer(receiveInstantiationResult);
    }
  }

  // User shell pages can write their own Module.instantiateWasm = function(imports, successCallback) callback
  // to manually instantiate the Wasm module themselves. This allows pages to run the instantiation parallel
  // to any other async startup actions they are performing.
  // Also pthreads and wasm workers initialize the wasm instance through this path.
  if (Module['instantiateWasm']) {
    try {
      var exports = Module['instantiateWasm'](info, receiveInstance);
      return exports;
    } catch(e) {
      err('Module.instantiateWasm callback failed with error: ' + e);
      return false;
    }
  }

  // If instantiation fails, reject the module ready promise.
  instantiateAsync().catch(readyPromiseReject);
  return {}; // no exports yet; we'll fill them in later
}

// Globals used by JS i64 conversions (see makeSetValue)
var tempDouble;
var tempI64;

// === Body ===

var ASM_CONSTS = {
  
};






  function callRuntimeCallbacks(callbacks) {
      while (callbacks.length > 0) {
        var callback = callbacks.shift();
        if (typeof callback == 'function') {
          callback(Module); // Pass the module as the first argument.
          continue;
        }
        var func = callback.func;
        if (typeof func == 'number') {
          if (callback.arg === undefined) {
            // Run the wasm function ptr with signature 'v'. If no function
            // with such signature was exported, this call does not need
            // to be emitted (and would confuse Closure)
            getWasmTableEntry(func)();
          } else {
            // If any function with signature 'vi' was exported, run
            // the callback with that signature.
            getWasmTableEntry(func)(callback.arg);
          }
        } else {
          func(callback.arg === undefined ? null : callback.arg);
        }
      }
    }

  function withStackSave(f) {
      var stack = stackSave();
      var ret = f();
      stackRestore(stack);
      return ret;
    }
  function demangle(func) {
      return func;
    }

  function demangleAll(text) {
      var regex =
        /\b_Z[\w\d_]+/g;
      return text.replace(regex,
        function(x) {
          var y = demangle(x);
          return x === y ? x : (y + ' [' + x + ']');
        });
    }

  function getWasmTableEntry(funcPtr) {
      // In -Os and -Oz builds, do not implement a JS side wasm table mirror for small
      // code size, but directly access wasmTable, which is a bit slower as uncached.
      return wasmTable.get(funcPtr);
    }

  function handleException(e) {
      // Certain exception types we do not treat as errors since they are used for
      // internal control flow.
      // 1. ExitStatus, which is thrown by exit()
      // 2. "unwind", which is thrown by emscripten_unwind_to_js_event_loop() and others
      //    that wish to return to JS event loop.
      if (e instanceof ExitStatus || e == 'unwind') {
        return EXITSTATUS;
      }
      quit_(1, e);
    }

  function jsStackTrace() {
      var error = new Error();
      if (!error.stack) {
        // IE10+ special cases: It does have callstack info, but it is only populated if an Error object is thrown,
        // so try that as a special-case.
        try {
          throw new Error();
        } catch(e) {
          error = e;
        }
        if (!error.stack) {
          return '(no stack trace available)';
        }
      }
      return error.stack.toString();
    }

  function setWasmTableEntry(idx, func) {
      wasmTable.set(idx, func);
    }

  function stackTrace() {
      var js = jsStackTrace();
      if (Module['extraStackTrace']) js += '\n' + Module['extraStackTrace']();
      return demangleAll(js);
    }

  function ___assert_fail(condition, filename, line, func) {
      abort('Assertion failed: ' + UTF8ToString(condition) + ', at: ' + [filename ? UTF8ToString(filename) : 'unknown filename', line, func ? UTF8ToString(func) : 'unknown function']);
    }

  function setErrNo(value) {
      HEAP32[((___errno_location())>>2)] = value;
      return value;
    }
  
  var SYSCALLS = {buffers:[null,[],[]],printChar:function(stream, curr) {
        var buffer = SYSCALLS.buffers[stream];
        if (curr === 0 || curr === 10) {
          (stream === 1 ? out : err)(UTF8ArrayToString(buffer, 0));
          buffer.length = 0;
        } else {
          buffer.push(curr);
        }
      },varargs:undefined,get:function() {
        SYSCALLS.varargs += 4;
        var ret = HEAP32[(((SYSCALLS.varargs)-(4))>>2)];
        return ret;
      },getStr:function(ptr) {
        var ret = UTF8ToString(ptr);
        return ret;
      },get64:function(low, high) {
        return low;
      }};
  function ___syscall_fcntl64(fd, cmd, varargs) {
  SYSCALLS.varargs = varargs;
  
      return 0;
    }

  function ___syscall_fstat64(fd, buf) {
  }

  function ___syscall_ioctl(fd, op, varargs) {
  SYSCALLS.varargs = varargs;
  
      return 0;
    }

  function ___syscall_lstat64(path, buf) {
  }

  function ___syscall_newfstatat(dirfd, path, buf, flags) {
  }

  function ___syscall_openat(dirfd, path, flags, varargs) {
  SYSCALLS.varargs = varargs;
  
  }

  function ___syscall_stat64(path, buf) {
  }

  function __emscripten_date_now() {
      return Date.now();
    }

  function __emscripten_throw_longjmp() { throw Infinity; }

  function __mmap_js(addr, len, prot, flags, fd, off, allocated, builtin) {
      return -52;
    }

  function __munmap_js(addr, len, prot, flags, fd, offset) {
    }

  function _abort() {
      abort('');
    }

  function _emscripten_get_heap_max() {
      // Stay one Wasm page short of 4GB: while e.g. Chrome is able to allocate
      // full 4GB Wasm memories, the size will wrap back to 0 bytes in Wasm side
      // for any code that deals with heap sizes, which would require special
      // casing all heap size related code to treat 0 specially.
      return 2147483648;
    }

  function emscripten_realloc_buffer(size) {
      try {
        // round size grow request up to wasm page size (fixed 64KB per spec)
        wasmMemory.grow((size - buffer.byteLength + 65535) >>> 16); // .grow() takes a delta compared to the previous size
        updateGlobalBufferAndViews(wasmMemory.buffer);
        return 1 /*success*/;
      } catch(e) {
      }
      // implicit 0 return to save code size (caller will cast "undefined" into 0
      // anyhow)
    }
  function _emscripten_resize_heap(requestedSize) {
      var oldSize = HEAPU8.length;
      requestedSize = requestedSize >>> 0;
      // With multithreaded builds, races can happen (another thread might increase the size
      // in between), so return a failure, and let the caller retry.
  
      // Memory resize rules:
      // 1.  Always increase heap size to at least the requested size, rounded up
      //     to next page multiple.
      // 2a. If MEMORY_GROWTH_LINEAR_STEP == -1, excessively resize the heap
      //     geometrically: increase the heap size according to
      //     MEMORY_GROWTH_GEOMETRIC_STEP factor (default +20%), At most
      //     overreserve by MEMORY_GROWTH_GEOMETRIC_CAP bytes (default 96MB).
      // 2b. If MEMORY_GROWTH_LINEAR_STEP != -1, excessively resize the heap
      //     linearly: increase the heap size by at least
      //     MEMORY_GROWTH_LINEAR_STEP bytes.
      // 3.  Max size for the heap is capped at 2048MB-WASM_PAGE_SIZE, or by
      //     MAXIMUM_MEMORY, or by ASAN limit, depending on which is smallest
      // 4.  If we were unable to allocate as much memory, it may be due to
      //     over-eager decision to excessively reserve due to (3) above.
      //     Hence if an allocation fails, cut down on the amount of excess
      //     growth, in an attempt to succeed to perform a smaller allocation.
  
      // A limit is set for how much we can grow. We should not exceed that
      // (the wasm binary specifies it, so if we tried, we'd fail anyhow).
      var maxHeapSize = _emscripten_get_heap_max();
      if (requestedSize > maxHeapSize) {
        return false;
      }
  
      let alignUp = (x, multiple) => x + (multiple - x % multiple) % multiple;
  
      // Loop through potential heap size increases. If we attempt a too eager
      // reservation that fails, cut down on the attempted size and reserve a
      // smaller bump instead. (max 3 times, chosen somewhat arbitrarily)
      for (var cutDown = 1; cutDown <= 4; cutDown *= 2) {
        var overGrownHeapSize = oldSize * (1 + 0.2 / cutDown); // ensure geometric growth
        // but limit overreserving (default to capping at +96MB overgrowth at most)
        overGrownHeapSize = Math.min(overGrownHeapSize, requestedSize + 100663296 );
  
        var newSize = Math.min(maxHeapSize, alignUp(Math.max(requestedSize, overGrownHeapSize), 65536));
  
        var replacement = emscripten_realloc_buffer(newSize);
        if (replacement) {
  
          return true;
        }
      }
      return false;
    }

  var ENV = {};
  
  function getExecutableName() {
      return thisProgram || './this.program';
    }
  function getEnvStrings() {
      if (!getEnvStrings.strings) {
        // Default values.
        // Browser language detection #8751
        var lang = ((typeof navigator == 'object' && navigator.languages && navigator.languages[0]) || 'C').replace('-', '_') + '.UTF-8';
        var env = {
          'USER': 'web_user',
          'LOGNAME': 'web_user',
          'PATH': '/',
          'PWD': '/',
          'HOME': '/home/web_user',
          'LANG': lang,
          '_': getExecutableName()
        };
        // Apply the user-provided values, if any.
        for (var x in ENV) {
          // x is a key in ENV; if ENV[x] is undefined, that means it was
          // explicitly set to be so. We allow user code to do that to
          // force variables with default values to remain unset.
          if (ENV[x] === undefined) delete env[x];
          else env[x] = ENV[x];
        }
        var strings = [];
        for (var x in env) {
          strings.push(x + '=' + env[x]);
        }
        getEnvStrings.strings = strings;
      }
      return getEnvStrings.strings;
    }
  function _environ_get(__environ, environ_buf) {
      var bufSize = 0;
      getEnvStrings().forEach(function(string, i) {
        var ptr = environ_buf + bufSize;
        HEAP32[(((__environ)+(i * 4))>>2)] = ptr;
        writeAsciiToMemory(string, ptr);
        bufSize += string.length + 1;
      });
      return 0;
    }

  function _environ_sizes_get(penviron_count, penviron_buf_size) {
      var strings = getEnvStrings();
      HEAP32[((penviron_count)>>2)] = strings.length;
      var bufSize = 0;
      strings.forEach(function(string) {
        bufSize += string.length + 1;
      });
      HEAP32[((penviron_buf_size)>>2)] = bufSize;
      return 0;
    }

  function _exit(status) {
      // void _exit(int status);
      // http://pubs.opengroup.org/onlinepubs/000095399/functions/exit.html
      exit(status);
    }

  function _fd_close(fd) {
      return 0;
    }

  function _fd_read(fd, iov, iovcnt, pnum) {
      var stream = SYSCALLS.getStreamFromFD(fd);
      var num = SYSCALLS.doReadv(stream, iov, iovcnt);
      HEAP32[((pnum)>>2)] = num;
      return 0;
    }

  function _fd_seek(fd, offset_low, offset_high, whence, newOffset) {
  }

  function flush_NO_FILESYSTEM() {
      // flush anything remaining in the buffers during shutdown
      var buffers = SYSCALLS.buffers;
      if (buffers[1].length) SYSCALLS.printChar(1, 10);
      if (buffers[2].length) SYSCALLS.printChar(2, 10);
    }
  function _fd_write(fd, iov, iovcnt, pnum) {
      ;
      // hack to support printf in SYSCALLS_REQUIRE_FILESYSTEM=0
      var num = 0;
      for (var i = 0; i < iovcnt; i++) {
        var ptr = HEAP32[((iov)>>2)];
        var len = HEAP32[(((iov)+(4))>>2)];
        iov += 8;
        for (var j = 0; j < len; j++) {
          SYSCALLS.printChar(fd, HEAPU8[ptr+j]);
        }
        num += len;
      }
      HEAP32[((pnum)>>2)] = num;
      return 0;
    }

  function _setTempRet0(val) {
      setTempRet0(val);
    }
var ASSERTIONS = false;



/** @type {function(string, boolean=, number=)} */
function intArrayFromString(stringy, dontAddNull, length) {
  var len = length > 0 ? length : lengthBytesUTF8(stringy)+1;
  var u8array = new Array(len);
  var numBytesWritten = stringToUTF8Array(stringy, u8array, 0, u8array.length);
  if (dontAddNull) u8array.length = numBytesWritten;
  return u8array;
}

function intArrayToString(array) {
  var ret = [];
  for (var i = 0; i < array.length; i++) {
    var chr = array[i];
    if (chr > 0xFF) {
      if (ASSERTIONS) {
        assert(false, 'Character code ' + chr + ' (' + String.fromCharCode(chr) + ')  at offset ' + i + ' not in 0x00-0xFF.');
      }
      chr &= 0xFF;
    }
    ret.push(String.fromCharCode(chr));
  }
  return ret.join('');
}


var asmLibraryArg = {
  "__assert_fail": ___assert_fail,
  "__syscall_fcntl64": ___syscall_fcntl64,
  "__syscall_fstat64": ___syscall_fstat64,
  "__syscall_ioctl": ___syscall_ioctl,
  "__syscall_lstat64": ___syscall_lstat64,
  "__syscall_newfstatat": ___syscall_newfstatat,
  "__syscall_openat": ___syscall_openat,
  "__syscall_stat64": ___syscall_stat64,
  "_emscripten_date_now": __emscripten_date_now,
  "_emscripten_throw_longjmp": __emscripten_throw_longjmp,
  "_mmap_js": __mmap_js,
  "_munmap_js": __munmap_js,
  "abort": _abort,
  "emscripten_get_heap_max": _emscripten_get_heap_max,
  "emscripten_resize_heap": _emscripten_resize_heap,
  "environ_get": _environ_get,
  "environ_sizes_get": _environ_sizes_get,
  "exit": _exit,
  "fd_close": _fd_close,
  "fd_read": _fd_read,
  "fd_seek": _fd_seek,
  "fd_write": _fd_write,
  "setTempRet0": _setTempRet0
};
var asm = createWasm();
/** @type {function(...*):?} */
var ___wasm_call_ctors = Module["___wasm_call_ctors"] = function() {
  return (___wasm_call_ctors = Module["___wasm_call_ctors"] = Module["asm"]["__wasm_call_ctors"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_set_states = Module["_fsg_set_states"] = function() {
  return (_fsg_set_states = Module["_fsg_set_states"] = Module["asm"]["fsg_set_states"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_hash_iter = Module["_cmd_ln_hash_iter"] = function() {
  return (_cmd_ln_hash_iter = Module["_cmd_ln_hash_iter"] = Module["asm"]["cmd_ln_hash_iter"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _hash_iter_key = Module["_hash_iter_key"] = function() {
  return (_hash_iter_key = Module["_hash_iter_key"] = Module["asm"]["hash_iter_key"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _set_mdef = Module["_set_mdef"] = function() {
  return (_set_mdef = Module["_set_mdef"] = Module["asm"]["set_mdef"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _set_tmat = Module["_set_tmat"] = function() {
  return (_set_tmat = Module["_set_tmat"] = Module["asm"]["set_tmat"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _load_gmm = Module["_load_gmm"] = function() {
  return (_load_gmm = Module["_load_gmm"] = Module["asm"]["load_gmm"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ptm_mgau_init_s3file = Module["_ptm_mgau_init_s3file"] = function() {
  return (_ptm_mgau_init_s3file = Module["_ptm_mgau_init_s3file"] = Module["asm"]["ptm_mgau_init_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _s3file_rewind = Module["_s3file_rewind"] = function() {
  return (_s3file_rewind = Module["_s3file_rewind"] = Module["asm"]["s3file_rewind"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _s2_semi_mgau_init_s3file = Module["_s2_semi_mgau_init_s3file"] = function() {
  return (_s2_semi_mgau_init_s3file = Module["_s2_semi_mgau_init_s3file"] = Module["asm"]["s2_semi_mgau_init_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ms_mgau_init_s3file = Module["_ms_mgau_init_s3file"] = function() {
  return (_ms_mgau_init_s3file = Module["_ms_mgau_init_s3file"] = Module["asm"]["ms_mgau_init_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_str_r = Module["_cmd_ln_str_r"] = function() {
  return (_cmd_ln_str_r = Module["_cmd_ln_str_r"] = Module["asm"]["cmd_ln_str_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_float_r = Module["_cmd_ln_float_r"] = function() {
  return (_cmd_ln_float_r = Module["_cmd_ln_float_r"] = Module["asm"]["cmd_ln_float_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_int_r = Module["_cmd_ln_int_r"] = function() {
  return (_cmd_ln_int_r = Module["_cmd_ln_int_r"] = Module["asm"]["cmd_ln_int_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_retain = Module["_cmd_ln_retain"] = function() {
  return (_cmd_ln_retain = Module["_cmd_ln_retain"] = Module["asm"]["cmd_ln_retain"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _logmath_retain = Module["_logmath_retain"] = function() {
  return (_logmath_retain = Module["_logmath_retain"] = Module["asm"]["logmath_retain"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_free_r = Module["_cmd_ln_free_r"] = function() {
  return (_cmd_ln_free_r = Module["_cmd_ln_free_r"] = Module["asm"]["cmd_ln_free_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _logmath_free = Module["_logmath_free"] = function() {
  return (_logmath_free = Module["_logmath_free"] = Module["asm"]["logmath_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _s3file_free = Module["_s3file_free"] = function() {
  return (_s3file_free = Module["_s3file_free"] = Module["asm"]["s3file_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _bin_mdef_read_s3file = Module["_bin_mdef_read_s3file"] = function() {
  return (_bin_mdef_read_s3file = Module["_bin_mdef_read_s3file"] = Module["asm"]["bin_mdef_read_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _malloc = Module["_malloc"] = function() {
  return (_malloc = Module["_malloc"] = Module["asm"]["malloc"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _free = Module["_free"] = function() {
  return (_free = Module["_free"] = Module["asm"]["free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_parse_r = Module["_cmd_ln_parse_r"] = function() {
  return (_cmd_ln_parse_r = Module["_cmd_ln_parse_r"] = Module["asm"]["cmd_ln_parse_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_init = Module["_cmd_ln_init"] = function() {
  return (_cmd_ln_init = Module["_cmd_ln_init"] = Module["asm"]["cmd_ln_init"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_exists_r = Module["_cmd_ln_exists_r"] = function() {
  return (_cmd_ln_exists_r = Module["_cmd_ln_exists_r"] = Module["asm"]["cmd_ln_exists_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_type_r = Module["_cmd_ln_type_r"] = function() {
  return (_cmd_ln_type_r = Module["_cmd_ln_type_r"] = Module["asm"]["cmd_ln_type_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_set_str_r = Module["_cmd_ln_set_str_r"] = function() {
  return (_cmd_ln_set_str_r = Module["_cmd_ln_set_str_r"] = Module["asm"]["cmd_ln_set_str_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_set_int_r = Module["_cmd_ln_set_int_r"] = function() {
  return (_cmd_ln_set_int_r = Module["_cmd_ln_set_int_r"] = Module["asm"]["cmd_ln_set_int_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _cmd_ln_set_float_r = Module["_cmd_ln_set_float_r"] = function() {
  return (_cmd_ln_set_float_r = Module["_cmd_ln_set_float_r"] = Module["asm"]["cmd_ln_set_float_r"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var ___errno_location = Module["___errno_location"] = function() {
  return (___errno_location = Module["___errno_location"] = Module["asm"]["__errno_location"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_trans_add = Module["_fsg_model_trans_add"] = function() {
  return (_fsg_model_trans_add = Module["_fsg_model_trans_add"] = Module["asm"]["fsg_model_trans_add"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_tag_trans_add = Module["_fsg_model_tag_trans_add"] = function() {
  return (_fsg_model_tag_trans_add = Module["_fsg_model_tag_trans_add"] = Module["asm"]["fsg_model_tag_trans_add"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_null_trans_add = Module["_fsg_model_null_trans_add"] = function() {
  return (_fsg_model_null_trans_add = Module["_fsg_model_null_trans_add"] = Module["asm"]["fsg_model_null_trans_add"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _hash_table_iter_next = Module["_hash_table_iter_next"] = function() {
  return (_hash_table_iter_next = Module["_hash_table_iter_next"] = Module["asm"]["hash_table_iter_next"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_word_id = Module["_fsg_model_word_id"] = function() {
  return (_fsg_model_word_id = Module["_fsg_model_word_id"] = Module["asm"]["fsg_model_word_id"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_word_add = Module["_fsg_model_word_add"] = function() {
  return (_fsg_model_word_add = Module["_fsg_model_word_add"] = Module["asm"]["fsg_model_word_add"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _logmath_log = Module["_logmath_log"] = function() {
  return (_logmath_log = Module["_logmath_log"] = Module["asm"]["logmath_log"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_init = Module["_fsg_model_init"] = function() {
  return (_fsg_model_init = Module["_fsg_model_init"] = Module["asm"]["fsg_model_init"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_free = Module["_fsg_model_free"] = function() {
  return (_fsg_model_free = Module["_fsg_model_free"] = Module["asm"]["fsg_model_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _fsg_model_retain = Module["_fsg_model_retain"] = function() {
  return (_fsg_model_retain = Module["_fsg_model_retain"] = Module["asm"]["fsg_model_retain"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _logmath_exp = Module["_logmath_exp"] = function() {
  return (_logmath_exp = Module["_logmath_exp"] = Module["asm"]["logmath_exp"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _jsgf_grammar_free = Module["_jsgf_grammar_free"] = function() {
  return (_jsgf_grammar_free = Module["_jsgf_grammar_free"] = Module["asm"]["jsgf_grammar_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _jsgf_get_rule = Module["_jsgf_get_rule"] = function() {
  return (_jsgf_get_rule = Module["_jsgf_get_rule"] = Module["asm"]["jsgf_get_rule"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _jsgf_get_public_rule = Module["_jsgf_get_public_rule"] = function() {
  return (_jsgf_get_public_rule = Module["_jsgf_get_public_rule"] = Module["asm"]["jsgf_get_public_rule"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _jsgf_build_fsg = Module["_jsgf_build_fsg"] = function() {
  return (_jsgf_build_fsg = Module["_jsgf_build_fsg"] = Module["asm"]["jsgf_build_fsg"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _jsgf_parse_string = Module["_jsgf_parse_string"] = function() {
  return (_jsgf_parse_string = Module["_jsgf_parse_string"] = Module["asm"]["jsgf_parse_string"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _logmath_init = Module["_logmath_init"] = function() {
  return (_logmath_init = Module["_logmath_init"] = Module["asm"]["logmath_init"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_config = Module["_ps_init_config"] = function() {
  return (_ps_init_config = Module["_ps_init_config"] = Module["asm"]["ps_init_config"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_args = Module["_ps_args"] = function() {
  return (_ps_args = Module["_ps_args"] = Module["asm"]["ps_args"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_cleanup = Module["_ps_init_cleanup"] = function() {
  return (_ps_init_cleanup = Module["_ps_init_cleanup"] = Module["asm"]["ps_init_cleanup"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_fe = Module["_ps_init_fe"] = function() {
  return (_ps_init_fe = Module["_ps_init_fe"] = Module["asm"]["ps_init_fe"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_feat_s3file = Module["_ps_init_feat_s3file"] = function() {
  return (_ps_init_feat_s3file = Module["_ps_init_feat_s3file"] = Module["asm"]["ps_init_feat_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_acmod_pre = Module["_ps_init_acmod_pre"] = function() {
  return (_ps_init_acmod_pre = Module["_ps_init_acmod_pre"] = Module["asm"]["ps_init_acmod_pre"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_acmod_post = Module["_ps_init_acmod_post"] = function() {
  return (_ps_init_acmod_post = Module["_ps_init_acmod_post"] = Module["asm"]["ps_init_acmod_post"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_dict_s3file = Module["_ps_init_dict_s3file"] = function() {
  return (_ps_init_dict_s3file = Module["_ps_init_dict_s3file"] = Module["asm"]["ps_init_dict_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_set_fsg = Module["_ps_set_fsg"] = function() {
  return (_ps_set_fsg = Module["_ps_set_fsg"] = Module["asm"]["ps_set_fsg"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init_grammar_s3file = Module["_ps_init_grammar_s3file"] = function() {
  return (_ps_init_grammar_s3file = Module["_ps_init_grammar_s3file"] = Module["asm"]["ps_init_grammar_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_set_jsgf_string = Module["_ps_set_jsgf_string"] = function() {
  return (_ps_set_jsgf_string = Module["_ps_set_jsgf_string"] = Module["asm"]["ps_set_jsgf_string"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_reinit_fe = Module["_ps_reinit_fe"] = function() {
  return (_ps_reinit_fe = Module["_ps_reinit_fe"] = Module["asm"]["ps_reinit_fe"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_init = Module["_ps_init"] = function() {
  return (_ps_init = Module["_ps_init"] = Module["asm"]["ps_init"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_retain = Module["_ps_retain"] = function() {
  return (_ps_retain = Module["_ps_retain"] = Module["asm"]["ps_retain"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_free = Module["_ps_free"] = function() {
  return (_ps_free = Module["_ps_free"] = Module["asm"]["ps_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_get_config = Module["_ps_get_config"] = function() {
  return (_ps_get_config = Module["_ps_get_config"] = Module["asm"]["ps_get_config"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_get_logmath = Module["_ps_get_logmath"] = function() {
  return (_ps_get_logmath = Module["_ps_get_logmath"] = Module["asm"]["ps_get_logmath"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_add_word = Module["_ps_add_word"] = function() {
  return (_ps_add_word = Module["_ps_add_word"] = Module["asm"]["ps_add_word"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_lookup_word = Module["_ps_lookup_word"] = function() {
  return (_ps_lookup_word = Module["_ps_lookup_word"] = Module["asm"]["ps_lookup_word"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_start_utt = Module["_ps_start_utt"] = function() {
  return (_ps_start_utt = Module["_ps_start_utt"] = Module["asm"]["ps_start_utt"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_process_float32 = Module["_ps_process_float32"] = function() {
  return (_ps_process_float32 = Module["_ps_process_float32"] = Module["asm"]["ps_process_float32"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_end_utt = Module["_ps_end_utt"] = function() {
  return (_ps_end_utt = Module["_ps_end_utt"] = Module["asm"]["ps_end_utt"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_get_hyp = Module["_ps_get_hyp"] = function() {
  return (_ps_get_hyp = Module["_ps_get_hyp"] = Module["asm"]["ps_get_hyp"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_iter = Module["_ps_seg_iter"] = function() {
  return (_ps_seg_iter = Module["_ps_seg_iter"] = Module["asm"]["ps_seg_iter"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_word = Module["_ps_seg_word"] = function() {
  return (_ps_seg_word = Module["_ps_seg_word"] = Module["asm"]["ps_seg_word"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_frames = Module["_ps_seg_frames"] = function() {
  return (_ps_seg_frames = Module["_ps_seg_frames"] = Module["asm"]["ps_seg_frames"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_prob = Module["_ps_seg_prob"] = function() {
  return (_ps_seg_prob = Module["_ps_seg_prob"] = Module["asm"]["ps_seg_prob"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_next = Module["_ps_seg_next"] = function() {
  return (_ps_seg_next = Module["_ps_seg_next"] = Module["asm"]["ps_seg_next"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_get_prob = Module["_ps_get_prob"] = function() {
  return (_ps_get_prob = Module["_ps_get_prob"] = Module["asm"]["ps_get_prob"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _ps_seg_free = Module["_ps_seg_free"] = function() {
  return (_ps_seg_free = Module["_ps_seg_free"] = Module["asm"]["ps_seg_free"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _s3file_init = Module["_s3file_init"] = function() {
  return (_s3file_init = Module["_s3file_init"] = Module["asm"]["s3file_init"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _tmat_init_s3file = Module["_tmat_init_s3file"] = function() {
  return (_tmat_init_s3file = Module["_tmat_init_s3file"] = Module["asm"]["tmat_init_s3file"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _setThrew = Module["_setThrew"] = function() {
  return (_setThrew = Module["_setThrew"] = Module["asm"]["setThrew"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var _saveSetjmp = Module["_saveSetjmp"] = function() {
  return (_saveSetjmp = Module["_saveSetjmp"] = Module["asm"]["saveSetjmp"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var stackSave = Module["stackSave"] = function() {
  return (stackSave = Module["stackSave"] = Module["asm"]["stackSave"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var stackRestore = Module["stackRestore"] = function() {
  return (stackRestore = Module["stackRestore"] = Module["asm"]["stackRestore"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var stackAlloc = Module["stackAlloc"] = function() {
  return (stackAlloc = Module["stackAlloc"] = Module["asm"]["stackAlloc"]).apply(null, arguments);
};

/** @type {function(...*):?} */
var dynCall_jiji = Module["dynCall_jiji"] = function() {
  return (dynCall_jiji = Module["dynCall_jiji"] = Module["asm"]["dynCall_jiji"]).apply(null, arguments);
};





// === Auto-generated postamble setup entry stuff ===



var calledRun;

/**
 * @constructor
 * @this {ExitStatus}
 */
function ExitStatus(status) {
  this.name = "ExitStatus";
  this.message = "Program terminated with exit(" + status + ")";
  this.status = status;
}

var calledMain = false;

dependenciesFulfilled = function runCaller() {
  // If run has never been called, and we should call run (INVOKE_RUN is true, and Module.noInitialRun is not false)
  if (!calledRun) run();
  if (!calledRun) dependenciesFulfilled = runCaller; // try this again later, after new deps are fulfilled
};

/** @type {function(Array=)} */
function run(args) {
  args = args || arguments_;

  if (runDependencies > 0) {
    return;
  }

  preRun();

  // a preRun added a dependency, run will be called later
  if (runDependencies > 0) {
    return;
  }

  function doRun() {
    // run may have just been called through dependencies being fulfilled just in this very frame,
    // or while the async setStatus time below was happening
    if (calledRun) return;
    calledRun = true;
    Module['calledRun'] = true;

    if (ABORT) return;

    initRuntime();

    readyPromiseResolve(Module);
    if (Module['onRuntimeInitialized']) Module['onRuntimeInitialized']();

    postRun();
  }

  if (Module['setStatus']) {
    Module['setStatus']('Running...');
    setTimeout(function() {
      setTimeout(function() {
        Module['setStatus']('');
      }, 1);
      doRun();
    }, 1);
  } else
  {
    doRun();
  }
}
Module['run'] = run;

/** @param {boolean|number=} implicit */
function exit(status, implicit) {
  EXITSTATUS = status;

  procExit(status);
}

function procExit(code) {
  EXITSTATUS = code;
  if (!keepRuntimeAlive()) {
    if (Module['onExit']) Module['onExit'](code);
    ABORT = true;
  }
  quit_(code, new ExitStatus(code));
}

if (Module['preInit']) {
  if (typeof Module['preInit'] == 'function') Module['preInit'] = [Module['preInit']];
  while (Module['preInit'].length > 0) {
    Module['preInit'].pop()();
  }
}

run();





// SoundSwallower JavaScript API code.
// our classes use delete() following embind usage:
// https://emscripten.org/docs/porting/connecting_cpp_and_javascript/embind.html#memory-management

const ARG_INTEGER = (1 << 1);
const ARG_FLOATING = (1 << 2);
const ARG_STRING = (1 << 3);
const ARG_BOOLEAN = (1 << 4);

const DEFAULT_MODEL = 'en-us';

// User can specify a default model, or none at all
if (typeof(Module.defaultModel) === 'undefined') {
    Module.defaultModel = DEFAULT_MODEL;
}
// User can also specify the base URL for models
if (typeof(Module.modelBase) === 'undefined') {
    if (ENVIRONMENT_IS_WEB) {
	Module.modelBase = "model/";
    }
    else {
	Module.modelBase = require("./model/index.js");
    }
}

/**
 * Configuration object for SoundSwallower recognizer.
 *
 * There is a fixed set of configuration values, which can be iterated
 * over using the iterator property.  Many have default values.
 */
class Config {
    /**
     * Create a configuration object.
     * @param {Object} [dict] - Initial configuration parameters and
     * values.  Some of the more common are noted below, the full list
     * can be found at
     * https://soundswallower.readthedocs.io/en/latest/config_params.html
     * @param {string} [dict.hmm=Module.get_model_path(Module.defaultModel)]
     *                 - Directory or base URL of acoustic model.
     * @param {string} [dict.loglevel="ERROR"] - Verbosity of logging.
     * @param {number} [dict.samprate=44100] - Sampling rate of input.
     */
    constructor(dict) {
	this.cmd_ln = Module._cmd_ln_parse_r(0, Module._ps_args(), 0, 0, 0);
	if (typeof(dict) === 'undefined') {
	    if (Module.defaultModel !== null)
		dict = { hmm: Module.get_model_path(Module.defaultModel) };
	    else
		return;
	}
	else if (Module.defaultModel !== null) {
	    if (!("hmm" in dict))
		dict.hmm = Module.get_model_path(Module.defaultModel);
	}
	for (const key in dict) {
	    this.set(key, dict[key]);
	}
    }
    /**
     * Free Emscripten memory associated with this Config.
     */
    delete() {
	if (this.cmd_ln)
	    Module._cmd_ln_free_r(this.cmd_ln);
	this.cmd_ln = 0;
    }
    normalize_key(key) {
	if (key.length > 0) {
	    if (key[0] == '_') {
		// Ask for underscore, get underscore
		return key;
	    }
	    else if (key[0] == '-') {
		// Ask for dash, get underscore or dash
		const under_key = "_" + key.substr(1);
		if (this.has(under_key))
		    return under_key;
		else
		    return key;
	    }
	    else {
		// No dash or underscore, try underscore then dash
		const under_key = "_" + key;
		if (this.has(under_key))
		    return under_key;
		const dash_key = "-" + key;
		if (this.has(dash_key))
		    return dash_key;
		return key;
	    }
	}
	else
	    return "";
    }
    normalize_ckey(ckey) {
	const key = UTF8ToString(ckey);
	if (key.length == 0)
	    return key;
	else if (key[0] == '-' || key[0] == '_')
	    return key.substr(1);
	return key;
    }
    /**
     * Set a configuration parameter.
     * @param {string} key - Parameter name.
     * @param {number|string} val - Parameter value.
     * @throws {ReferenceError} Throws ReferenceError if key is not a known parameter.
     */
    set(key, val) {
	const nkey = this.normalize_key(key);
	const ckey = allocateUTF8OnStack(nkey);
	const type = Module._cmd_ln_type_r(this.cmd_ln, ckey);
	if (type == 0) {
	    throw new ReferenceError("Unknown cmd_ln parameter "+key);
	}
	if (type & ARG_STRING) {
	    const cval = allocateUTF8OnStack(val);
	    Module._cmd_ln_set_str_r(this.cmd_ln, ckey, cval);
	}
	else if (type & ARG_FLOATING) {
	    Module._cmd_ln_set_float_r(this.cmd_ln, ckey, val);
	}
	else if (type & (ARG_INTEGER | ARG_BOOLEAN)) {
	    Module._cmd_ln_set_int_r(this.cmd_ln, ckey, val);
	}
	else {
	    return false;
	}
	return true;
    }
    /**
     * Get a configuration parameter's value.
     * @param {string} key - Parameter name.
     * @returns {number|string} Parameter value.
     * @throws {ReferenceError} Throws ReferenceError if key is not a known parameter.
     */
    get(key) {
	const ckey = allocateUTF8OnStack(this.normalize_key(key));
	const type = Module._cmd_ln_type_r(this.cmd_ln, ckey);
	if (type == 0) {
	    throw new ReferenceError("Unknown cmd_ln parameter "+key);
	}
	if (type & ARG_STRING) {
	    const val = Module._cmd_ln_str_r(this.cmd_ln, ckey);
	    if (val == 0)
		return null;
	    return UTF8ToString(val);
	}
	else if (type & ARG_FLOATING) {
	    return Module._cmd_ln_float_r(this.cmd_ln, ckey);
	}
	else if (type & ARG_INTEGER) {
	    return Module._cmd_ln_int_r(this.cmd_ln, ckey);
	}
	else if (type & ARG_BOOLEAN) {
	    return Boolean(Module._cmd_ln_int_r(this.cmd_ln, ckey));
	}
	else {
	    throw new TypeError("Unsupported type "+type+" for parameter"+key);
	}
    }
    /**
     * Get a model parameter with backoff to path inside current model.
     */
    model_file_path(key, modelfile) {
	const val = this.get(key);
	if (val != null)
	    return val;
	const hmmpath = this.get("hmm");
	if (hmmpath == null)
	    throw new Error("Could not get "+key+" from config or model directory");
	return hmmpath + "/" + modelfile;
    }
    /**
     * Test if a key is a known parameter.
     * @param {string} key - Key whose existence to check.
     */
    has(key) {
	const ckey = allocateUTF8OnStack(key);
	return Module._cmd_ln_exists_r(this.cmd_ln, ckey);
    }
    *[Symbol.iterator]() {
	let itor = Module._cmd_ln_hash_iter(this.cmd_ln);
	const seen = new Set();
	while (itor != 0) {
	    const ckey = Module._hash_iter_key(itor);
	    const key = this.normalize_ckey(ckey);
	    if (seen.has(key))
		continue;
	    seen.add(key);
	    itor = Module._hash_table_iter_next(itor);
	    yield key;
	}
    }
};

/**
 * Speech recognizer object.
 */
class Decoder {
    /**
     * Create the decoder.
     *
     * This can be called with a previously created Config
     * object, or with an Object containing configuration keys and
     * values from which a Config will be created.
     *
     * @param {Object|Config} [config] - Configuration parameters.
     */
    constructor(config) {
	if (config && typeof(config) == 'object' && 'cmd_ln' in config)
	    this.config = config;
	else
	    this.config = new Module.Config(...arguments);
	this.initialized = false;
	this.ps = Module._ps_init(0);
	if (this.ps == 0)
	    throw new Error("Failed to construct Decoder");
    }
    /**
     * (Re-)initialize the decoder asynchronously.
     * @param {Object|Config} [config] - New configuration parameters
     * to apply, if desired.
     * @returns {Promise} Promise resolved once decoder is ready.
     */
    async initialize(config) {
	if (this.ps == 0)
	    throw new Error("Decoder was somehow not constructed (ps==0)");
	if (config !== undefined) {
	    if (this.config)
		this.config.delete();
	    if (typeof(config) == 'object' && 'cmd_ln' in config)
		this.config = config;
	    else
		this.config = new Module.Config(...arguments);
	}
	await this.init_config();
	await this.init_fe();
	await this.init_feat();
	await this.init_acmod();
	await this.load_acmod_files();
	await this.init_dict();
	await this.init_grammar();

	this.initialized = true;
    }

    /**
     * Initialize decoder configuration.
     */
    async init_config() {
	await this.init_featparams()
	let rv = Module._ps_init_config(this.ps, this.config.cmd_ln);
	if (rv < 0)
	    throw new Error("Failed to initialize basic configuration");
	rv = Module._ps_init_cleanup(this.ps);
	if (rv < 0)
	    throw new Error("Failed to clean up decoder internals");
    }

    /**
     * Read feature parameters from acoustic model.
     */
    async init_featparams() {
	const featparams = this.config.model_file_path("featparams", "feat.params");
	for await (const pair of read_featparams(featparams)) {
	    if (this.config.has(pair[0])) /* Sometimes it doesn't */
		this.config.set(pair[0], pair[1]);
	}
    }
    
    /**
     * Create front-end from configuration.
     */
    async init_fe() {
	const rv = Module._ps_init_fe(this.ps);
	if (rv == 0)
	    throw new Error("Failed to initialize frontend");
    }

    /**
     * Create dynamic feature module from configuration.
     */
    async init_feat() {
	let rv;
	try {
	    const lda_path = this.config.model_file_path("lda", "feature_transform");
	    const lda = await load_to_s3file(lda_path);
	    rv = Module._ps_init_feat_s3file(this.ps, lda);
	}
	catch (e) {
	    rv = Module._ps_init_feat_s3file(this.ps, 0);
	}
	if (rv == 0)
	    throw new Error("Failed to initialize feature module");
    }

    /**
     * Create acoustic model from configuration.
     */
    async init_acmod() {
	const rv = Module._ps_init_acmod_pre(this.ps);
	if (rv == 0)
	    throw new Error("Failed to initialize acoustic model");
    }

    /**
     * Load acoustic model files
     */
    async load_acmod_files() {
	await this.load_mdef();
	const tmat = this.config.model_file_path("tmat", "transition_matrices");
	await this.load_tmat(tmat);
	const means = this.config.model_file_path("mean", "means");
	const variances = this.config.model_file_path("var", "variances");
	const sendump = this.config.model_file_path("sendump", "sendump");
	const mixw = this.config.model_file_path("mixw", "mixture_weights");
	await this.load_gmm(means, variances, sendump, mixw);
	const rv = Module._ps_init_acmod_post(this.ps);
	if (rv < 0)
	    throw new Error("Failed to initialize acoustic scoring");
    }

    /**
     * Load binary model definition file
     */
    async load_mdef() {
	/* Prefer mixw.bin if available. */
	var mdef_path, s3f;
	try {
	    mdef_path = this.config.model_file_path("mdef", "mdef.bin");
	    s3f = await load_to_s3file(mdef_path);
	}
	catch (e) {
	    try {
		mdef_path = this.config.model_file_path("mdef", "mdef.txt");
		s3f = await load_to_s3file(mdef_path);
	    }
	    catch (ee) {
		mdef_path = this.config.model_file_path("mdef", "mdef");
		s3f = await load_to_s3file(mdef_path);
	    }
	}
        const mdef = Module._bin_mdef_read_s3file(s3f, this.config.get("cionly"));
	Module._s3file_free(s3f);
	if (mdef == 0)
	    throw new Error("Failed to read mdef");
	Module._set_mdef(this.ps, mdef);
    }

    /**
     * Load transition matrices
     */
    async load_tmat(tmat_path) {
	const s3f = await load_to_s3file(tmat_path);
	const logmath = Module._ps_get_logmath(this.ps);
	const tpfloor = this.config.get("tmatfloor");
	const tmat = Module._tmat_init_s3file(s3f, logmath, tpfloor);
	Module._s3file_free(s3f);
	if (tmat == 0)
	    throw new Error("Failed to read tmat");
	Module._set_tmat(this.ps, tmat);
    }

    /**
     * Load Gaussian mixture models
     */
    async load_gmm(means_path, variances_path, sendump_path, mixw_path) {
	const means = await load_to_s3file(means_path);
	const variances = await load_to_s3file(variances_path);
	var sendump, mixw;
	/* Prefer sendump if available. */
	try {
	    sendump = await load_to_s3file(sendump_path);
	    mixw = 0;
	}
	catch (e) {
	    sendump = 0;
	    mixw = await load_to_s3file(mixw_path);
	}
	if (Module._load_gmm(this.ps, means, variances, mixw, sendump) < 0)
	    throw new Error("Failed to load GMM parameters");
    }

    /**
     * Load dictionary from configuration.
     */
    async init_dict() {
	const dict_path = this.config.model_file_path("dict", "dict.txt");
	const dict = await load_to_s3file(dict_path);
	let fdict;
	try {
	    const fdict_path = this.config.model_file_path("fdict", "noisedict");
	    fdict = await load_to_s3file(fdict_path);
	}
	catch (e) {
	    fdict = 0;
	}
	const rv = Module._ps_init_dict_s3file(this.ps, dict, fdict);
	if (rv == 0)
	    throw new Error("Failed to initialize dictionaries");
    }

    /**
     * Load grammar from configuration.
     */
    async init_grammar() {
	let fsg = 0, jsgf = 0;
	const jsgf_path = this.config.get("jsgf");
	if (jsgf_path != null)
	    jsgf = await load_to_s3file(jsgf_path)
	const fsg_path = this.config.get("fsg");
	if (fsg_path != null)
	    fsg = await load_to_s3file(fsg_path)
	if (fsg || jsgf) {
	    const rv = Module._ps_init_grammar_s3file(this.ps, fsg, jsgf);
	    if (rv < 0)
		throw new Error("Failed to initialize grammar");
	}
    }

    /**
     * Throw an error if decoder is not initialized.
     * @throws {Error} If decoder is not initialized.
     */
    assert_initialized() {
	if (!this.initialized)
	    throw new Error("Decoder not yet initialized");
    }

    /**
     * Re-initialize only the audio feature extraction.
     * @returns {Promise} Promise resolved once reinitialized.
     */
    async reinitialize_audio() {
	this.assert_initialized();
	Module._ps_reinit_fe(this.ps, 0);
    }

    /**
     * Release the Emscripten memory associated with a Decoder.
     */
    delete() {
	if (this.config)
	    this.config.delete();
	if (this.ps)
	    Module._ps_free(this.ps);
	this.ps = 0;
    }

    /**
     * Start processing input asynchronously.
     * @returns {Promise} Promise resolved once processing is started.
     */
    async start() {
	this.assert_initialized();
	if (Module._ps_start_utt(this.ps) < 0) {
	    throw new Error("Failed to start utterance processing");
	}
    }

    /**
     * Finish processing input asynchronously.
     * @returns {Promise} Promise resolved once processing is finished.
     */
    async stop() {
	this.assert_initialized();
	if (Module._ps_end_utt(this.ps) < 0) {
	    throw new Error("Failed to stop utterance processing");
	}
    }

    /**
     * Process a block of audio data asynchronously.
     * @param {Float32Array} pcm - Audio data, in float32 format, in
     * the range [-1.0, 1.0].
     * @returns {Promise<number>} Promise resolved to the number of
     * frames processed.
     */
    async process(pcm, no_search=false, full_utt=false) {
	this.assert_initialized();
	const pcm_bytes = pcm.length * pcm.BYTES_PER_ELEMENT;
	const pcm_addr = Module._malloc(pcm_bytes);
	const pcm_u8 = new Uint8Array(pcm.buffer);
	// Emscripten documentation fails to mention that this
	// function specifically takes a Uint8Array
	writeArrayToMemory(pcm_u8, pcm_addr);
	const rv = Module._ps_process_float32(this.ps, pcm_addr, pcm_bytes / 4,
					    no_search, full_utt);
	Module._free(pcm_addr);
	if (rv < 0) {
	    throw new Error("Utterance processing failed");
	}
	return rv;
    }

    /**
     * Get the currently recognized text.
     * @returns {string} Currently recognized text.
     */
    get_hyp() {
	this.assert_initialized();
	return UTF8ToString(Module._ps_get_hyp(this.ps, 0));
    }

    /**
     * Get the current recognition result as a word segmentation.
     * @returns {Array<Object>} Array of Objects for the words
     * recognized, each with the keys `word`, `start` and `end`.
     */
    get_hypseg() {
	this.assert_initialized();
	let itor = Module._ps_seg_iter(this.ps);
	const config = Module._ps_get_config(this.ps);
	const frate = Module._cmd_ln_int_r(config, allocateUTF8OnStack("-frate"));
	const seg = [];
	while (itor != 0) {
	    const frames = stackAlloc(8);
	    Module._ps_seg_frames(itor, frames, frames + 4);
	    const start_frame = getValue(frames, 'i32');
	    const end_frame = getValue(frames + 4, 'i32');
	    const seg_item = {
		word: ccall('ps_seg_word', 'string', ['number'], [itor]),
		start: start_frame / frate,
		end: end_frame / frate
	    };
	    seg.push(seg_item);
	    itor = Module._ps_seg_next(itor);
	}
	return seg;
    }

    /**
     * Look up a word in the pronunciation dictionary.
     * @param {string} word - Text of word to look up.
     * @returns {string} - Space-separated list of phones, or `null` if
     * word is not in the dictionary.
     */
    lookup_word(word) {
	this.assert_initialized();
	const cword = allocateUTF8OnStack(word);
	const cpron = Module._ps_lookup_word(this.ps, cword);
	if (cpron == 0)
	    return null;
	return UTF8ToString(cpron);
    }
    
    /**
     * Add a word to the pronunciation dictionary asynchronously.
     * @param {string} word - Text of word to add.
     * @param {string} pron - Pronunciation of word as space-separated list of phonemes.
     * @param {number} update - Update decoder immediately (set to
     * false when adding a list of words, except for the last word).
     * @returns {Promise} - Promise resolved once word has been added.
     */
    async add_word(word, pron, update=true) {
	this.assert_initialized();
	const cword = allocateUTF8OnStack(word);
	const cpron = allocateUTF8OnStack(pron);
	const wid = Module._ps_add_word(this.ps, cword, cpron, update);
	if (wid < 0)
	    throw new Error("Failed to add word "+word+" with pronunciation "+
			    pron+" to the dictionary.");
	return wid;
    }

    /**
     * Create a finite-state grammar from a list of transitions.
     * @param {string} name - Name of grammar.
     * @param {number} start_state - Index of starting state.
     * @param {number} final_state - Index of ending state.
     * @param {Array<Object>} transitions - Array of transitions, each
     * of which is an Object with the keys `from`, `to`, `word`, and
     * `prob`.  The word must exist in the dictionary.
     * @returns {Object} Newly created grammar - you *must* free this
     * by calling its delete() method once it is no longer needed,
     * such as after passing to set_fsg().
     */
    create_fsg(name, start_state, final_state, transitions) {
	this.assert_initialized();
	const logmath = Module._ps_get_logmath(this.ps);
	const config = Module._ps_get_config(this.ps);
	const lw = Module._cmd_ln_float_r(config, allocateUTF8OnStack("-lw"));
	let n_state = 0;
	for (const t of transitions) {
	    n_state = Math.max(n_state, t.from, t.to);
	}
	n_state++;
	const fsg = ccall('fsg_model_init',
			'number', ['string', 'number', 'number', 'number'],
			[name, logmath, lw, n_state]);
	Module._fsg_set_states(fsg, start_state, final_state);
	for (const t of transitions) {
	    let logprob = 0;
	    if ('prob' in t) {
		logprob = Module._logmath_log(logmath, t.prob);
	    }
	    if ('word' in t) {
		const wid = ccall('fsg_model_word_add', 'number',
				['number', 'string'],
				[fsg, t.word]);
		if (wid == -1) {
		    Module._fsg_model_free(fsg);
		    return 0;
		}
		Module._fsg_model_trans_add(fsg, t.from, t.to, logprob, wid);
	    }
	    else {
		Module._fsg_model_null_trans_add(fsg, t.from, t.to, logprob);
	    }
	}
	return {
	    fsg: fsg,
	    delete() {
		Module._fsg_model_free(this.fsg);
		this.fsg = 0;
	    }
	};
    }

    /**
     * Create a grammar from JSGF.
     * @param {string} jsgf_string - String containing JSGF grammar.
     * @param {string} [toprule] - Name of starting rule for grammar,
     * if not specified, the first public rule will be used.
     * @returns {Object} Newly created grammar - you *must* free this
     * by calling its delete() method once it is no longer needed,
     * such as after passing to set_fsg().
     */
    parse_jsgf(jsgf_string, toprule=null) {
	this.assert_initialized();
	const logmath = Module._ps_get_logmath(this.ps);
	const config = Module._ps_get_config(this.ps);
	const lw = Module._cmd_ln_float_r(config, allocateUTF8OnStack("-lw"));
	const cjsgf = allocateUTF8OnStack(jsgf_string);
	const jsgf = Module._jsgf_parse_string(cjsgf, 0);
	if (jsgf == 0)
	    throw new Error("Failed to parse JSGF");
	let rule;
	if (toprule !== null) {
	    const crule = allocateUTF8OnStack(toprule);
	    rule = Module._jsgf_get_rule(jsgf, crule);
	    if (rule == 0)
		throw new Error("Failed to find top rule " + toprule);
	}
	else {
	    rule = Module._jsgf_get_public_rule(jsgf);
	    if (rule == 0)
		throw new Error("No public rules found in JSGF");
	}
	const fsg = Module._jsgf_build_fsg(jsgf, rule, logmath, lw);
	Module._jsgf_grammar_free(jsgf);
	return {
	    fsg: fsg,
	    delete() {
		Module._fsg_model_free(this.fsg);
		this.fsg = 0;
	    }
	};
    }

    /**
     * Set the grammar for recognition, asynchronously.
     * @param {Object} fsg - Grammar produced by parse_jsgf() or
     * create_fsg().  You must call its delete() method after
     * passing it here if you do not intend to reuse it.
     * @returns {Promise} Promise fulfilled once grammar is updated.
     */
    async set_fsg(fsg) {
	this.assert_initialized();
	if (Module._ps_set_fsg(this.ps, "_default", fsg.fsg) != 0) {
	    throw new Error("Failed to set FSG in decoder");
	}
    }
};

/**
 * Generate [key,value] pairs from feat.params file/URL.
 */
async function* read_featparams(featparams) {
    let fpdata;
    if (ENVIRONMENT_IS_WEB) {
	const response = await fetch(featparams);
	if (response.ok)
	    fpdata = await response.text();
	else
	    throw new Error("Failed to fetch " + featparams + " :"
			    + response.statusText);
    }
    else {
	const fs = require("fs/promises");
	fpdata = await fs.readFile(featparams, {encoding: "utf8"});
    }
    const line_re = /^.*$/mg;
    const arg_re = /"([^"]*)"|'([^'])'|(\S+)/g;
    let key = null;
    for (const m of fpdata.matchAll(line_re)) {
	const line = m[0].trim()
	for (const arg of line.matchAll(arg_re)) {
	    const token = arg[1] ?? arg[2] ?? arg[3];
	    if (token == '#')
		break;
	    if (key !== null) {
		yield [key, token];
		key = null;
	    }
	    else
		key = token;
	}
    }
    if (key !== null)
	throw new Error("Odd number of arguments in "+featparams);
}

/**
 * Load a file from disk or Internet and make it into an s3file_t.
 */
async function load_to_s3file(path) {
    let blob_u8;
    if (ENVIRONMENT_IS_WEB) {
	const response = await fetch(path);
	if (response.ok) {
	    const blob = await response.blob();
	    const blob_buf = await blob.arrayBuffer();
	    blob_u8 = new Uint8Array(blob_buf);
	}
	else
	    throw new Error("Failed to fetch " + path + " :" + response.statusText);
    }
    else {
	const fs = require("fs/promises");
	// FIXME: Should read directly to emscripten memory... how?
	const blob = await fs.readFile(path);
	blob_u8 = new Uint8Array(blob.buffer);
    }
    const blob_len = blob_u8.length + 1;
    const blob_addr = Module._malloc(blob_len);
    if (blob_addr == 0)
	throw new Error("Failed to allocate "+blob_len+" bytes for "+path);
    writeArrayToMemory(blob_u8, blob_addr);
    // Ensure it is NUL-terminated in case someone treats it as a string
    HEAP8[blob_addr + blob_len] = 0;
    // But exclude the trailing NUL from file size so it works normally
    return Module._s3file_init(blob_addr, blob_len - 1);
}

/**
 * Get a model or model file from the built-in model path.
 *
 * The base path can be set by modifying the `modelBase` property of
 * the module object, at initialization or any other time.  Or you can
 * also just override this function if you have special needs.
 *
 * This function is used by `Decoder` (and also `Config`) to find the
 * default model, which is equivalent to `Model.modelBase +
 * Model.defaultModel`.
 *
 * @param {string} subpath - path to model directory or parameter
 * file, e.g. "en-us", "en-us/variances", etc
 * @returns {string} concatenated path. Note this is a simple string
 * concatenation on the Web, so ensure that `modelBase` has a trailing
 * slash if it is a directory.
 */
function get_model_path(subpath) {
    if (ENVIRONMENT_IS_WEB) {
	return Module.modelBase + subpath;
    }
    else {
	const path = require("path");
	return path.join(Module.modelBase, subpath);
    }
}

Module.get_model_path = get_model_path;
Module.Config = Config;
Module.Decoder = Decoder;


  return Module.ready
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
  module.exports = Module;
else if (typeof define === 'function' && define['amd'])
  define([], function() { return Module; });
else if (typeof exports === 'object')
  exports["Module"] = Module;
