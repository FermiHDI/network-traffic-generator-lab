'use strict'

const Fastify = require('fastify');
const fastlyStatic = require('@fastify/static');
const fastifyRedis = require('@fastify/redis');
const path = require('node:path')

if (process.argv.length < 3) {
  console.error('Expected at least one argument!');
  process.exit(1);
}

// Scope Vars
const appPort = 3000;
let redisServer = 'redis'

let redisUpdated = false;

console.log(`command line arguments: ${process.argv}`);
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i] === '--redis') {
    redisServer = process.argv[i + 1];
    redisUpdated = true;
    break;
  }
}
if (!redisUpdated) {
  console.error(`Redis server not specified, using default: ${redisServer}`);
}

// Build server
const fastify = Fastify({
  logger: true,
  pluginTimeout: 30000
});
fastify.register(fastlyStatic, {
  root: path.join(__dirname, 'public'),
  prefix: '/public/'
});
fastify.register(fastifyRedis, {
  host: redisServer
});

fastify.get('/', (request, reply) => {
  const { redis } = fastify
  redis.set('test_key', Math.floor(Math.random() * 1000));
  redis.get('test_key', (err, val) => {
    if (err) {
      request.log.error(err);
    } else {
      request.log.info(`Redis get test_key: ${val}`);
    }
  });
  reply.sendFile('index.html');
})

fastify.listen({ port: appPort, host: '0.0.0.0' }, (err) => {
  if (err) {
    fastify.log.error(err.message);
    throw err;
  }
});
