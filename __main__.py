from .ssai import main
import sys
try:
    main()
except KeyboardInterrupt as e:
    print 'Quitting'
    sys.exit(0)

