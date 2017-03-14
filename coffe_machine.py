class CoffeeMachine(object):

    WATER_MAX_AMOUNT = 10000
    MILK_MAX_AMOUNT = 2000
    CURRENT_AMOUNT_OF_WATER = 0
    CURRENT_AMOUNT_OF_MILK = 0

    def add_water(self, water_amount):
        self.CURRENT_AMOUNT_OF_WATER +=water_amount
        if self.CURRENT_AMOUNT_OF_WATER > self.WATER_MAX_AMOUNT:
            self.CURRENT_AMOUNT_OF_WATER -=water_amount
            print 'You exceeded the maximum capacity'

    def add_milk(self, milk_amount):
        self.CURRENT_AMOUNT_OF_MILK +=milk_amount
        if self.CURRENT_AMOUNT_OF_MILK > self.MILK_MAX_AMOUNT:
            self.CURRENT_AMOUNT_OF_MILK -=milk_amount
            print 'You exceeded the maximum capacity' 

    def add_sugar(self):
        pass

    def large_coffee(self, milk=False, sugar=0):
        WATER_NEED = 500
        MILK_NEED = 150

        if self.CURRENT_AMOUNT_OF_WATER >= WATER_NEED:
            self.CURRENT_AMOUNT_OF_WATER -= WATER_NEED
            for x in range(sugar):
                self.add_sugar()
            if milk:
                if self.CURRENT_AMOUNT_OF_MILK >= MILK_NEED:
                    self.CURRENT_AMOUNT_OF_MILK -= MILK_NEED
                    self._get_ready_time(WATER_NEED + MILK_NEED)
                    return
                else:
                    print 'No enough milk'
                    return
            self._get_ready_time(WATER_NEED)
        else:
            print 'No enough water'


    def middle_coffee(self, milk=False, sugar=0):
        WATER_NEED = 250
        MILK_NEED = 100

        if self.CURRENT_AMOUNT_OF_WATER >= WATER_NEED:
            self.CURRENT_AMOUNT_OF_WATER -= WATER_NEED
            if milk:
                if self.CURRENT_AMOUNT_OF_MILK >= MILK_NEED:
                    self.CURRENT_AMOUNT_OF_MILK -= MILK_NEED
                    return
                else:
                    print 'No enough milk'
                    return
            for x in range(sugar):
                self.add_sugar()
            self._get_ready_time(WATER_NEED + MILK_NEED)
        else:
            print 'No enough water'

    def espresso(self):
        WATER_NEED = 125

        if self.CURRENT_AMOUNT_OF_WATER >= WATER_NEED:
            self.CURRENT_AMOUNT_OF_WATER -= WATER_NEED
            self._get_ready_time(WATER_NEED)
        else:
            print 'No enough water'

    def _get_ready_time(self, water_mass):
        WATER_HEAT_CAPACITY = 4200
        AVERAGE_TEMPERATURE = 80
        POWER = 220
        time_to_go = ((water_mass/.1000) * WATER_HEAT_CAPACITY * AVERAGE_TEMPERATURE) / float(POWER)
        print '{} seconds to go'.format(int(time_to_go))

if __name__ == '__main__':
    a = CoffeeMachine()
    a.add_water(6000)
    a.espresso()

