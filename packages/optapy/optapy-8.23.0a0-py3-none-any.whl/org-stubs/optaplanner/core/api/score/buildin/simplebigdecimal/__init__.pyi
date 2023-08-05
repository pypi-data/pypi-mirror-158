import decimal
import java.lang
import java.math
import org.kie.api.runtime.rule
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.holder
import typing



class SimpleBigDecimalScore(org.optaplanner.core.api.score.AbstractScore['SimpleBigDecimalScore']):
    """
    public final class SimpleBigDecimalScore extends :class:`~org.optaplanner.core.api.score.AbstractScore`<:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`>
    
        This :class:`~org.optaplanner.core.api.score.Score` is based on 1 level of
        :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`
        constraints.
    
        This class is immutable.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.Score`, :meth:`~serialized`
    """
    ZERO: typing.ClassVar['SimpleBigDecimalScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore` ZERO
    
    
    """
    ONE: typing.ClassVar['SimpleBigDecimalScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore` ONE
    
    
    """
    def add(self, simpleBigDecimalScore: 'SimpleBigDecimalScore') -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.add`
            Returns a Score whose value is (this + addend).
        
            Parameters:
                addend (:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`): value to be added to this Score
        
            Returns:
                this + addend
        
        
        """
        ...
    def compareTo(self, simpleBigDecimalScore: 'SimpleBigDecimalScore') -> int: ...
    def divide(self, double: float) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.divide`
            Returns a Score whose value is (this / divisor). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double divisor should have no
            impact on the returned scale/precision.
        
            Parameters:
                divisor (double): value by which this Score is to be divided
        
            Returns:
                this / divisor
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def getScore(self) -> java.math.BigDecimal:
        """
            The total of the broken negative constraints and fulfilled positive constraints. Their weight is included in the total.
            The score is usually a negative number because most use cases only have negative constraints.
        
            Returns:
                higher is better, usually negative, 0 if no constraints are broken/fulfilled
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def isFeasible(self) -> bool:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.isFeasible`
            A :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is feasible if it has no broken hard constraints
            and :meth:`~org.optaplanner.core.api.score.Score.isSolutionInitialized` is true. Simple scores
            (:class:`~org.optaplanner.core.api.score.buildin.simple.SimpleScore`,
            :class:`~org.optaplanner.core.api.score.buildin.simplelong.SimpleLongScore`,
            :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`) are always feasible, if their
            :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0.
        
            Returns:
                true if the hard score is 0 or higher and the :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0.
        
        
        """
        ...
    def multiply(self, double: float) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.multiply`
            Returns a Score whose value is (this * multiplicand). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double multiplicand should have
            no impact on the returned scale/precision.
        
            Parameters:
                multiplicand (double): value to be multiplied by this Score.
        
            Returns:
                this * multiplicand
        
        
        """
        ...
    def negate(self) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.negate`
            Returns a Score whose value is (- this).
        
            Returns:
                - this
        
        
        """
        ...
    @staticmethod
    def of(bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'SimpleBigDecimalScore': ...
    @staticmethod
    def ofUninitialized(int: int, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'SimpleBigDecimalScore': ...
    @staticmethod
    def parseScore(string: str) -> 'SimpleBigDecimalScore': ...
    def power(self, double: float) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.power`
            Returns a Score whose value is (this ^ exponent). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double exponent should have no
            impact on the returned scale/precision.
        
            Parameters:
                exponent (double): value by which this Score is to be powered
        
            Returns:
                this ^ exponent
        
        
        """
        ...
    def subtract(self, simpleBigDecimalScore: 'SimpleBigDecimalScore') -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.subtract`
            Returns a Score whose value is (this - subtrahend).
        
            Parameters:
                subtrahend (:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`): value to be subtracted from this Score
        
            Returns:
                this - subtrahend, rounded as necessary
        
        
        """
        ...
    def toLevelNumbers(self) -> typing.List[java.lang.Number]:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toLevelNumbers`
            Returns an array of numbers representing the Score. Each number represents 1 score level. A greater score level uses a
            lower array index than a lesser score level.
        
            When rounding is needed, each rounding should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
            The length of the returned array must be stable for a specific :class:`~org.optaplanner.core.api.score.Score`
            implementation.
        
            For example: :code:`-0hard/-7soft` returns :code:`new int{-0, -7}`
        
            The level numbers do not contain the :meth:`~org.optaplanner.core.api.score.Score.getInitScore`. For example:
            :code:`-3init/-0hard/-7soft` also returns :code:`new int{-0, -7}`
        
            Returns:
                never null
        
        
        """
        ...
    def toShortString(self) -> str:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toShortString`
            Like
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`,
            but trims score levels which have a zero weight. For example 0hard/-258soft returns -258soft.
        
            Do not use this format to persist information as text, use
            :meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`
            instead, so it can be parsed reliably.
        
            Returns:
                never null
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def withInitScore(self, int: int) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.withInitScore`
            For example :code:`0hard/-8soft` with :code:`-7` returns :code:`-7init/0hard/-8soft`.
        
            Parameters:
                newInitScore (int): always negative (except in statistical calculations), 0 if all planning variables are initialized
        
            Returns:
                equals score except that :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is set to :code:`newInitScore`
        
        
        """
        ...
    def zero(self) -> 'SimpleBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.zero`
            Returns a Score, all levels of which are zero.
        
            Returns:
                never null
        
        
        """
        ...

class SimpleBigDecimalScoreHolder(org.optaplanner.core.api.score.holder.ScoreHolder[SimpleBigDecimalScore]):
    """
    :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated?is`(:meth:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated.html?is`=true) public interface SimpleBigDecimalScoreHolder extends :class:`~org.optaplanner.core.api.score.holder.ScoreHolder`<:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`>
    
        Deprecated, for removal: This API element is subject to removal in a future version.
        Score DRL is deprecated and will be removed in a future major version of OptaPlanner. See
        :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.www.optaplanner.org.learn.drl`.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`
    """
    def addConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weight (:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): never null, higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def impactScore(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
        """
        ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated and
            multiplied with the weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): at least 0
        
        
        """
        ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` multiplied with the
            weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (:class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): at least 0
        
        
        """
        ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.buildin.simplebigdecimal")``.

    SimpleBigDecimalScore: typing.Type[SimpleBigDecimalScore]
    SimpleBigDecimalScoreHolder: typing.Type[SimpleBigDecimalScoreHolder]
