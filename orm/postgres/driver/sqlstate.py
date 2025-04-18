SQLSTATE_MESSAGES = {
    '00000': 'successful completion',
    '01000': 'warning',
    '0100C': 'dynamic result sets returned',
    '01008': 'implicit zero bit padding',
    '01003': 'null value eliminated in set function',
    '01007': 'privilege not granted',
    '01006': 'privilege not revoked',
    '01004': 'string data right truncation',
    '01P01': 'deprecated feature',
    '02000': 'no data',
    '02001': 'no additional dynamic result sets returned',
    '03000': 'sql statement not yet complete',
    '08000': 'connection exception',
    '08003': 'connection does not exist',
    '08006': 'connection failure',
    '08001': 'sqlclient unable to establish sqlconnection',
    '08004': 'sqlserver rejected establishment of sqlconnection',
    '08007': 'transaction resolution unknown',
    '08P01': 'protocol violation',
    '09000': 'triggered action exception',
    '0A000': 'feature not supported',
    '0B000': 'invalid transaction initiation',
    '0F000': 'locator exception',
    '0F001': 'invalid locator specification',
    '0L000': 'invalid grantor',
    '0LP01': 'invalid grant operation',
    '0P000': 'invalid role specification',
    '0Z000': 'diagnostics exception',
    '0Z002': 'stacked diagnostics accessed without active handler',
    '20000': 'case not found',
    '21000': 'cardinality violation',
    '22000': 'data exception',
    '2202E': 'array subscript error',
    '22021': 'character not in repertoire',
    '22008': 'datetime field overflow',
    '22012': 'division by zero',
    '22005': 'error in assignment',
    '2200B': 'escape character conflict',
    '22022': 'indicator overflow',
    '22015': 'interval field overflow',
    '2201E': 'invalid argument for logarithm',
    '22014': 'invalid argument for ntile function',
    '22016': 'invalid argument for nth value function',
    '2201F': 'invalid argument for power function',
    '2201G': 'invalid argument for width bucket function',
    '22018': 'invalid character value for cast',
    '22007': 'invalid datetime format',
    '22019': 'invalid escape character',
    '2200D': 'invalid escape octet',
    '22025': 'invalid escape sequence',
    '22P06': 'nonstandard use of escape character',
    '22010': 'invalid indicator parameter value',
    '22023': 'invalid parameter value',
    '22013': 'invalid preceding or following size',
    '2201B': 'invalid regular expression',
    '2201W': 'invalid row count in limit clause',
    '2201X': 'invalid row count in result offset clause',
    '2202H': 'invalid tablesample argument',
    '2202G': 'invalid tablesample repeat',
    '22009': 'invalid time zone displacement value',
    '2200C': 'invalid use of escape character',
    '2200G': 'most specific type mismatch',
    '22004': 'null value not allowed',
    '22002': 'null value no indicator parameter',
    '22003': 'numeric value out of range',
    '2200H': 'sequence generator limit exceeded',
    '22026': 'string data length mismatch',
    '22001': 'string data right truncation',
    '22011': 'substring error',
    '22027': 'trim error',
    '22024': 'unterminated C string',
    '2200F': 'zero length character string',
    '22P01': 'floating point exception',
    '22P02': 'invalid text representation',
    '22P03': 'invalid binary representation',
    '22P04': 'bad copy file format',
    '22P05': 'untranslatable character',
    '2200L': 'not an xml document',
    '2200M': 'invalid xml document',
    '2200N': 'invalid xml content',
    '2200S': 'invalid xml comment',
    '2200T': 'invalid xml processing instruction',
    '22030': 'duplicate json object key value',
    '22031': 'invalid argument for sql json datetime function',
    '22032': 'invalid json text',
    '22033': 'invalid sql json subscript',
    '22034': 'more than one sql json item',
    '22035': 'no sql json item',
    '22036': 'non numeric sql json item',
    '22037': 'non unique keys in a json object',
    '22038': 'singleton sql json item required',
    '22039': 'sql json array not found',
    '2203A': 'sql json member not found',
    '2203B': 'sql json number not found',
    '2203C': 'sql json object not found',
    '2203D': 'too many json array elements',
    '2203E': 'too many json object members',
    '2203F': 'sql json scalar required',
    '2203G': 'sql json item cannot be cast to target type',
    '23000': 'integrity constraint violation',
    '23001': 'restrict violation',
    '23502': 'not null violation',
    '23503': 'foreign key violation',
    '23505': 'unique violation',
    '23514': 'check violation',
    '23P01': 'exclusion violation',
    '24000': 'invalid cursor state',
    '25000': 'invalid transaction state',
    '25001': 'active sql transaction',
    '25002': 'branch transaction already active',
    '25008': 'held cursor requires same isolation level',
    '25003': 'inappropriate access mode for branch transaction',
    '25004': 'inappropriate isolation level for branch transaction',
    '25005': 'no active sql transaction for branch transaction',
    '25006': 'read only sql transaction',
    '25007': 'schema and data statement mixing not supported',
    '25P01': 'no active sql transaction',
    '25P02': 'in failed sql transaction',
    '25P03': 'idle in transaction session timeout',
    '25P04': 'transaction timeout',
    '26000': 'invalid sql statement name',
    '27000': 'triggered data change violation',
    '28000': 'invalid authorization specification',
    '28P01': 'invalid password',
    '2B000': 'dependent privilege descriptors still exist',
    '2BP01': 'dependent objects still exist',
    '2D000': 'invalid transaction termination',
    '2F000': 'sql routine exception',
    '2F005': 'function executed no return statement',
    '2F002': 'modifying sql data not permitted',
    '2F003': 'prohibited sql statement attempted',
    '2F004': 'reading sql data not permitted',
    '34000': 'invalid cursor name',
    '38000': 'external routine exception',
    '38001': 'containing sql not permitted',
    '38002': 'modifying sql data not permitted',
    '38003': 'prohibited sql statement attempted',
    '38004': 'reading sql data not permitted',
    '39000': 'external routine invocation exception',
    '39001': 'invalid sqlstate returned',
    '39004': 'null value not allowed',
    '39P01': 'trigger protocol violated',
    '39P02': 'srf protocol violated',
    '39P03': 'event trigger protocol violated',
    '3B000': 'savepoint exception',
    '3B001': 'invalid savepoint specification',
    '3D000': 'invalid catalog name',
    '3F000': 'invalid schema name',
    '40000': 'transaction rollback',
    '40001': 'serialization failure',
    '40002': 'transaction integrity constraint violation',
    '40003': 'statement completion unknown',
    '40P01': 'deadlock detected',
    '42000': 'syntax error or access rule violation',
    '42601': 'syntax error',
    '42501': 'insufficient privilege',
    '42846': 'cannot coerce',
    '42803': 'grouping error',
    '42P20': 'windowing error',
    '42P19': 'invalid recursion',
    '42830': 'invalid foreign key',
    '42602': 'invalid name',
    '42622': 'name too long',
    '42939': 'reserved name',
    '42804': 'datatype mismatch',
    '42P18': 'indeterminate datatype',
    '42P21': 'collation mismatch',
    '42P22': 'indeterminate collation',
    '42809': 'wrong object type',
    '428C9': 'generated always',
    '42703': 'undefined column',
    '42883': 'undefined function',
    '42P01': 'undefined table',
    '42P02': 'undefined parameter',
    '42704': 'undefined object',
    '42701': 'duplicate column',
    '42P03': 'duplicate cursor',
    '42P04': 'duplicate database',
    '42723': 'duplicate function',
    '42P05': 'duplicate prepared statement',
    '42P06': 'duplicate schema',
    '42P07': 'duplicate table',
    '42712': 'duplicate alias',
    '42710': 'duplicate object',
    '42702': 'ambiguous column',
    '42725': 'ambiguous function',
    '42P08': 'ambiguous parameter',
    '42P09': 'ambiguous alias',
    '42P10': 'invalid column reference',
    '42611': 'invalid column definition',
    '42P11': 'invalid cursor definition',
    '42P12': 'invalid database definition',
    '42P13': 'invalid function definition',
    '42P14': 'invalid prepared statement definition',
    '42P15': 'invalid schema definition',
    '42P16': 'invalid table definition',
    '42P17': 'invalid object definition',
    '44000': 'with check option violation',
    '53000': 'insufficient resources',
    '53100': 'disk full',
    '53200': 'out of memory',
    '53300': 'too many connections',
    '53400': 'configuration limit exceeded',
    '54000': 'program limit exceeded',
    '54001': 'statement too complex',
    '54011': 'too many columns',
    '54023': 'too many arguments',
    '55000': 'object not in prerequisite state',
    '55006': 'object in use',
    '55P02': 'cant change runtime param',
    '55P03': 'lock not available',
    '55P04': 'unsafe new enum value usage',
    '57000': 'operator intervention',
    '57014': 'query canceled',
    '57P01': 'admin shutdown',
    '57P02': 'crash shutdown',
    '57P03': 'cannot connect now',
    '57P04': 'database dropped',
    '57P05': 'idle session timeout',
    '58000': 'system error',
    '58030': 'io error',
    '58P01': 'undefined file',
    '58P02': 'duplicate file',
    'F0000': 'config file error',
    'F0001': 'lock file exists',
    'HV000': 'fdw error',
    'HV005': 'fdw column name not found',
    'HV002': 'fdw dynamic parameter value needed',
    'HV010': 'fdw function sequence error',
    'HV021': 'fdw inconsistent descriptor information',
    'HV024': 'fdw invalid attribute value',
    'HV007': 'fdw invalid column name',
    'HV008': 'fdw invalid column number',
    'HV004': 'fdw invalid data type',
    'HV006': 'fdw invalid data type descriptors',
    'HV091': 'fdw invalid descriptor field identifier',
    'HV00B': 'fdw invalid handle',
    'HV00C': 'fdw invalid option index',
    'HV00D': 'fdw invalid option name',
    'HV090': 'fdw invalid string length or buffer length',
    'HV00A': 'fdw invalid string format',
    'HV009': 'fdw invalid use of null pointer',
    'HV014': 'fdw too many handles',
    'HV001': 'fdw out of memory',
    'HV00P': 'fdw no schemas',
    'HV00J': 'fdw option name not found',
    'HV00K': 'fdw reply handle',
    'HV00Q': 'fdw schema not found',
    'HV00R': 'fdw table not found',
    'HV00L': 'fdw unable to create execution',
    'HV00M': 'fdw unable to create reply',
    'HV00N': 'fdw unable to establish connection',
    'P0000': 'plpgsql error',
    'P0001': 'raise exception',
    'P0002': 'no data found',
    'P0003': 'too many rows',
    'P0004': 'assert failure',
    'XX000': 'internal error',
    'XX001': 'data corrupted',
    'XX002': 'index corrupted',
}
