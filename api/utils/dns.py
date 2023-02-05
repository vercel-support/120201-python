
import random
import logging
from datetime import datetime
import dns
import dns.query
import dns.resolver
from dns.exception import DNSException

# Create a custom logger that logs to a file located in ../data/dns.log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

DNS_SERVERS = ["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4"]

class DNS(object):

    def __init__(self):
        self.mResolver = dns.resolver.Resolver()
        self.mResolver.timeout = 1
        self.mResolver.lifetime = 0.5
        self.mResolver.nameservers = random.sample(DNS_SERVERS, 1)
        self.spec_query_type = ['CNAME', 'TXT', 'MX', 'NS', 'SRV', 'CAA']

    def query(self, domain, query_type="A"):
        """Query the DNS record for the given record type and domain
        """
        try:
            query_type = query_type.upper()
            answer = self.mResolver.resolve(domain, query_type, raise_on_no_answer=False)
            answer_raw = answer.chaining_result.answer.to_text()
            logger.info("resolved response data => {}".format(answer_raw))
            if query_type in self.spec_query_type:
                records = [data.to_text() for data in answer]
            else:
                records = [data.address for data in answer]
            return { "type": "success" ,"message": records}
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                dns.resolver.NoNameservers, dns.exception.Timeout) as warning:
            logger.warning("resolved warning => {}, domain={}".format(warning, domain))
            return { "type": "warning" ,"message": warning}
        except (DNSException, ValueError) as error:
            logger.error("resolved error => {} domain={}".format(error, domain))
            return { "type": "error" ,"message": error}
        except Exception as error:
            logger.error("resolved error => {} domain={}".format(error, domain))
            return { "type": "error" ,"message": error}

    def is_valid(self, domain, query_type="A") -> bool:
        try:
            self.mResolver.resolve(domain, query_type, raise_on_no_answer=False)
            return True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                dns.resolver.NoNameservers, dns.exception.Timeout) as error:
            logger.warning("resolved error => {}".format(error))
        return False
