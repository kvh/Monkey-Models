import numpy as N
from scipy.stats import poisson
import random, math

guid = 0

"""
Agent-Based Model of monkey grooming behaviors.
All dates and times in minutes.
"""

class Monkey(object):
    guid = 0
    """Represents a single monkey"""
    def __init__(self, sex, birthdate, mother, father, rank, health):
        global guid
        self.id = guid
        guid += 1
        self.sex = sex
        self.birthdate = birthdate
        self.mother = mother
        self.father = father
        self.rank = rank
        self.health = health
    
    def __repr__(self):
        s = "----------\n"
        s+= "Monkey %d\n"%self.id
        s+= "----------\n"
        s+= "sex: %s\n" % self.sex
        s+= "birthdate: %d\n" % self.birthdate
        s+= "rank: %d\n" % self.rank
        s+= "health: %d\n" % self.health
        s+= "mother: %s\n" % self.mother.id if self.mother else ''
        s+= "father: %s\n" % self.father.id if self.father else ''
        return s
        
    @classmethod
    def create_random_monkey(cls, age_range=(1, 20), rank_range=(1, 10), health_range=(1,10)):
        sex = 'm' if random.random() > .5 else 'f'
        birthdate = random.randint(*age_range)
        rank = random.randint(*rank_range)
        health = random.randint(*health_range)
        return Monkey(sex, birthdate, None, None, rank, health)
    
    def make_offspring(self, father, birthdate=0):
        if self.sex != 'f':
            raise TypeError
        m = Monkey.create_random_monkey()
        m.birthdate = birthdate
        m.mother = self
        m.father = father
        return m
            
        
    def age_diff(self, other):
        return other.birthdate - self.birthdate
        
    def rank_diff(self, other):
        return self.rank - other.rank
        
    def health_diff(self, other):
        return self.health - other.health
        
    def same_sex(self, other):
        return int(self.sex == other.sex)
        

class Climate(object):
    """Represents a monthly climate model"""
    def __init__(self, monthly_rain, monthly_temp):
        self.monthly_rain = monthly_rain
        self.monthly_temp = monthly_temp
            

class GroomingModel(object):
    """Provides a model for determing the frequency with which two monkeys groom, given their covariates."""
    def __init__(self):
        pass
        
    def get_groomings(groomer, groomed, duration):
        pass
        
class PoissonLinearGroomingModel(GroomingModel):
    """Provides a simple linear model for the rate at which one monkey grooms another"""
    def __init__(self, covariate_methods, coefs, base_rate=1):
        super(PoissonLinearGroomingModel, self).__init__()
        self.covariate_methods = covariate_methods
        self.coefs = coefs
        self.base_rate = base_rate
        
    def determine_grooming_rate(self, groomer, groomed):
        rate = self.base_rate
        for coef, cv in zip(self.coefs, self.covariate_methods):
            rate += coef * getattr(groomer, cv)(groomed)
        return math.exp(rate)
        
    def get_groomings(self, groomer, groomed, environment, duration):
        duration_in_days = duration/(60 * 24)
        rate = self.determine_grooming_rate(groomer, groomed)
        return poisson.rvs(rate*duration_in_days, size=1)
        
    
    
class Population(object):
    """Represents a population of monkeys"""
    def __init__(self, size, grooming_model):
        self.size = size
        self.monkeys = []
        self.grooming_rates = N.zeros((size, size))
        self.social_distances = N.zeros((size, size))
        self.grooming_model = grooming_model
        
    def init_population_random(self):
        """This will provide a population w random characteristics and no family structure"""
        for i in range(self.size):
            new_monkey = Monkey.create_random_monkey()
            print new_monkey
            self.monkeys.append(new_monkey)
            
    def init_population_organically(self):
        """ This will provide a population w random characteristics 
            and organically grown (and highly inbred) family structure.
        """
        curr_date = 0
        adam = Monkey.create_random_monkey()
        adam.sex = 'm'
        adam.birthdate = 0
        eve = Monkey.create_random_monkey()
        eve.sex = 'f'
        eve.birthdate = 0
        curr_mother = eve
        curr_father = adam
        self.monkeys.append(adam)
        self.monkeys.append(eve)
        while len(self.monkeys) < self.size:
            curr_date += 60*24*365*5
            new_mother = curr_mother
            new_father = curr_father
            for i in range(random.randint(1, 3)):
                curr_date += 60*24*365
                offspring = curr_mother.make_offspring(curr_father, curr_date)
                self.monkeys.append(offspring)
                if offspring.sex == 'f':
                    new_mother = offspring
                else:
                    new_father = offspring
            curr_mother = new_mother
            curr_father = new_father
        self.monkeys = self.monkeys[:self.size]
        for m in self.monkeys:
            print m
        
        
class Environment(object):
    """Represents the monkey environment. All times in minutes."""
    def __init__(self, climate, time_resolution):
        """ climate: Climate object for environment
            time_resolution: size of time step of environment, in minutes
        """
        self.climate = climate
        self.time_resolution = time_resolution
        
    def init_simulation(self, size, grooming_model):
        self.pop = Population(size, grooming_model)
        self.pop.init_population_organically()
        
    def run_simulation(self, time_periods):
        for i in range(time_periods):
            print "-------------------"
            print "Starting period %d"%i
            print "-------------------"
            self.groom_all()
            
    def groom_all(self):
        for minky in self.pop.monkeys:
            for munky in self.pop.monkeys:
                if minky is munky:
                    continue
                groomings = self.pop.grooming_model.get_groomings(minky, munky, self, self.time_resolution)
                print "Monkey %d groomed monkey %d %d times"%(minky.id, munky.id, groomings)
            


def main():
    # set up climate with monthly rainfall and temp
    climate = Climate([random.randint(0,10) for i in range(12)], [random.randint(20, 30) for i in range(12)])
    
    # create environment
    environ = Environment(climate, 60*24)
    
    # set up linear covariates
    cvars = ['age_diff', 'rank_diff', 'health_diff', 'same_sex']
    coefs = [ -.0000001, # for age diff: we expect younger monkeys to groom older monkeys more often
              -.2, # rank diff: we expect lower ranked monkeys to groom higher ranked monkeys more often
              -.1, # health diff: we expect healthier monkeys to groom sicklier monkeys LESS often
              .3, # same sex: we expect same sex monkeys to groom each other more often
              ]
    # create grooming model
    mdl = PoissonLinearGroomingModel(cvars, coefs)
    
    # initialize environment
    environ.init_simulation(20, mdl)
    
    # run simulation
    environ.run_simulation(10)


if __name__ == '__main__':
    main()


        
        